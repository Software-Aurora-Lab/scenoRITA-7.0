# /apollo/modules/map/hdmap/hdmap_impl.h
# /apollo/modules/map/hdmap/hdmap_impl.cc

import pickle
from dataclasses import dataclass
from functools import lru_cache
from math import atan2, pi
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import networkx as nx
from shapely.geometry import LineString, Point
from shapely.geometry.base import BaseGeometry

from config import MAPS_DIR, SUPPORTED_MAPS
from modules.common_msgs.map_msgs.map_crosswalk_pb2 import Crosswalk
from modules.common_msgs.map_msgs.map_junction_pb2 import Junction
from modules.common_msgs.map_msgs.map_lane_pb2 import Lane, LaneBoundary
from modules.common_msgs.map_msgs.map_overlap_pb2 import Overlap
from modules.common_msgs.map_msgs.map_pb2 import Map
from modules.common_msgs.map_msgs.map_signal_pb2 import Signal
from modules.common_msgs.map_msgs.map_stop_sign_pb2 import StopSign
from mymath.kdtree import KDTree, KDTreeParams

__loaded_instances = dict()


@dataclass
class SegmentInfo:
    lane_id: str
    segment_index: int


@dataclass
class PositionEstimate:
    lane_id: str
    s: float


def load_map_service(map_name: str, refresh=False) -> "MapService":
    assert (
        map_name in SUPPORTED_MAPS
    ), f"Unsupported map {map_name}. Expected one of {SUPPORTED_MAPS}"
    map_bin = Path(MAPS_DIR, map_name, "base_map.bin")
    map_pic = Path(MAPS_DIR, map_name, "base_map.pickle")

    assert map_bin.exists(), f"Requested map {map_name} does not exist."

    if not map_pic.exists() or refresh:
        #
        instance = MapService()
        instance.load_map_from_file(str(map_bin))
        # save to pickle
        with open(map_pic, "wb") as fp:
            pickle.dump(instance, fp)
        # save in memory
        __loaded_instances[map_name] = instance
    elif map_name not in __loaded_instances:
        with open(map_pic, "rb") as fp:
            instance = pickle.load(fp)
            __loaded_instances[map_name] = instance

    return __loaded_instances[map_name]


def is_allowed_to_cross(boundary: LaneBoundary):
    for boundary_type in boundary.boundary_type:
        # DOTTED_YELLOW = 1
        # DOTTED_WHITE = 2
        if boundary_type.types[0] not in [1, 2]:
            return False
    return True


class MapService:
    kSearchRadius = 3.0
    kMaxHeadingDiff = 1.0

    FLAGS_min_length_for_lane_change = 1.0

    lane_kdtree: KDTree
    junction_kdtree: KDTree
    crosswalk_kdtree: KDTree
    signal_kdtree: KDTree
    stop_sign_kdtree: KDTree

    def __init__(self) -> None:
        self.lane_table: Dict[str, Lane] = dict()
        self.junction_table: Dict[str, Junction] = dict()
        self.crosswalk_table: Dict[str, Crosswalk] = dict()
        self.signal_table: Dict[str, Signal] = dict()
        self.stop_sign_table: Dict[str, StopSign] = dict()
        self.overlap_table: Dict[str, Overlap] = dict()

        self.lane_boxes: Dict[BaseGeometry, SegmentInfo] = dict()
        self.junction_boxes: Dict[BaseGeometry, str] = dict()
        self.crosswalk_boxes: Dict[BaseGeometry, str] = dict()
        self.signal_boxes: Dict[BaseGeometry, str] = dict()
        self.stop_sign_boxes: Dict[BaseGeometry, str] = dict()

        self.non_junction_lanes: List[str] = list()

        self.routing_graph = nx.DiGraph()
        self.obs_routing_graph = nx.DiGraph()

    def load_map_from_file(self, filename: str):
        map = Map()
        with open(filename, "rb") as fp:
            map.ParseFromString(fp.read())
        self.load_map_from_proto(map)

    def load_map_from_proto(self, map: Map):
        obj_table_map = [
            (map.lane, self.lane_table),
            (map.junction, self.junction_table),
            (map.crosswalk, self.crosswalk_table),
            (map.signal, self.signal_table),
            (map.stop_sign, self.stop_sign_table),
            (map.overlap, self.overlap_table),
        ]
        for objects, table_name in obj_table_map:
            for obj in objects:
                table_name[obj.id.id] = obj

        self.build_lane_segment_kd_tree()
        self.build_routing_graph()
        self.find_non_junction_lanes()
        # self.build_junction_polygon_kd_tree()
        # self.build_signal_segment_kd_tree()
        # self.build_crosswalk_polygon_kd_tree()
        # self.build_stop_sign_segment_kd_tree()

    def get_lanes(self, point: Optional[Point], distance=0.0) -> Iterable[str]:
        if distance == 0.0:
            return self.lane_table.keys()
        return self.__get_lanes(point, distance)

    @lru_cache(maxsize=20)
    def __get_lanes(self, point: Point, distance: float) -> Iterable[str]:
        nearby_objects = self.lane_kdtree.get_objects(point, distance)
        result = set()
        for obj in nearby_objects:
            result.add(self.lane_boxes[obj].lane_id)
        return result

    def get_junctions(self, point: Point, distance=0.0) -> Iterable[str]:
        if distance == 0.0:
            return self.junction_table.keys()
        raise NotImplementedError()

    def get_crosswalks(self, point: Point, distance=0.0) -> Iterable[str]:
        if distance == 0.0:
            return self.crosswalk_table.keys()
        raise NotImplementedError()

    def get_signals(self, point: Point, distance=0.0) -> Iterable[str]:
        if distance == 0.0:
            return self.signal_table.keys()
        raise NotImplementedError()

    def get_stop_signs(self, point: Point, distance=0.0) -> Iterable[str]:
        if distance == 0.0:
            return self.stop_sign_table.keys()
        raise NotImplementedError()

    def get_lane_by_id(self, lane_id: str) -> Lane:
        return self.lane_table[lane_id]

    def get_lane_central_curve_by_id(self, lane_id: str) -> LineString:
        lane_obj = self.get_lane_by_id(lane_id)
        cv = lane_obj.central_curve
        cv_points = cv.segment[0].line_segment
        return LineString([[x.x, x.y] for x in cv_points.point])

    def get_lane_boundary_types_by_id(self, lane_id: str) -> Tuple[int, int]:
        lane_obj = self.get_lane_by_id(lane_id)
        return (
            lane_obj.left_boundary.boundary_type[0].types[0],
            lane_obj.right_boundary.boundary_type[0].types[0],
        )

    def get_lane_boundaries_by_id(self, lane_id: str) -> Tuple[LineString, LineString]:
        lane_obj = self.get_lane_by_id(lane_id)

        left_boundary_points: List[Tuple[float, float]] = list()
        right_boundary_points: List[Tuple[float, float]] = list()

        for result_container, boundary_obj in [
            (left_boundary_points, lane_obj.left_boundary),
            (right_boundary_points, lane_obj.right_boundary),
        ]:
            for segment in boundary_obj.curve.segment:
                for segment_point in segment.line_segment.point:
                    result_container.append((segment_point.x, segment_point.y))
        return LineString(left_boundary_points), LineString(right_boundary_points)

    def get_junction_by_id(self, junction_id: str):
        return self.junction_table[junction_id]

    def get_crosswalk_by_id(self, crosswalk_id: str):
        return self.crosswalk_table[crosswalk_id]

    def get_signal_by_id(self, signal_id: str):
        return self.signal_table[signal_id]

    def get_stop_sign_by_id(self, stop_sign_id: str):
        return self.stop_sign_table[stop_sign_id]

    def get_overlap_by_id(self, overlap_id: str):
        return self.overlap_table[overlap_id]

    def get_path_from(
        self, lane_id: str, forward_only=True, limit=15
    ) -> List[List[str]]:
        result: List[List[str]] = []
        if limit == 0:
            return result
        for _, target in self.routing_graph.edges(lane_id):
            edge_data = self.routing_graph.get_edge_data(lane_id, target)
            if forward_only and edge_data["direction_type"] in ["L", "R"]:
                continue
            result.append([lane_id, target])
            for path in self.get_path_from(target, forward_only, limit - 1):
                result.append([lane_id] + path)
        return result

    def find_non_junction_lanes(self) -> None:
        result = list()
        junction_overlap_ids = set()
        # find all overlap ids that are associated with junctions
        for junction in self.junction_table:
            junction_obj = self.junction_table[junction]
            for oid in junction_obj.overlap_id:
                junction_overlap_ids.add(oid.id)
        # find all lanes that are not associated with junctions
        for lane_id in self.lane_table:
            lane_obj = self.lane_table[lane_id]
            lane_overlap_ids = set([x.id for x in lane_obj.overlap_id])
            if lane_overlap_ids & junction_overlap_ids == set():
                result.append(lane_id)
        self.non_junction_lanes = result

    def build_routing_graph(self):
        # modules/routing/topo_creator/graph_creator.cc
        for lane_id in self.lane_table:
            pred = [x.id for x in self.lane_table[lane_id].predecessor_id]
            succ = [x.id for x in self.lane_table[lane_id].successor_id]
            l_neighbor = [
                x.id for x in self.lane_table[lane_id].left_neighbor_forward_lane_id
            ]
            r_neighbor = [
                x.id for x in self.lane_table[lane_id].right_neighbor_forward_lane_id
            ]
            for pid in pred:
                self.routing_graph.add_edge(pid, lane_id, direction_type="F")
                self.obs_routing_graph.add_edge(pid, lane_id)
            for pid in succ:
                self.routing_graph.add_edge(lane_id, pid, direction_type="F")
                self.obs_routing_graph.add_edge(lane_id, pid)

            if (
                self.lane_table[lane_id].length
                < MapService.FLAGS_min_length_for_lane_change
            ):
                continue

            for pid in l_neighbor:
                if is_allowed_to_cross(self.lane_table[pid].left_boundary):
                    self.routing_graph.add_edge(lane_id, pid, direction_type="L")
            for pid in r_neighbor:
                if is_allowed_to_cross(self.lane_table[pid].right_boundary):
                    self.routing_graph.add_edge(lane_id, pid, direction_type="R")

    def build_lane_segment_kd_tree(self):
        params = KDTreeParams(max_leaf_dimension=5.0, max_leaf_size=16)
        objects = set()
        for lane_id in self.lane_table:
            lane_obj = self.lane_table[lane_id]
            cv = lane_obj.central_curve
            cv_points = cv.segment[0].line_segment
            lst = LineString([[x.x, x.y] for x in cv_points.point])
            segments = list(map(LineString, zip(lst.coords[:-1], lst.coords[1:])))
            for index, segment in enumerate(segments):
                self.lane_boxes[segment] = SegmentInfo(lane_id, index)
                objects.add(segment)
        self.lane_kdtree = KDTree(objects, params)

    def build_junction_polygon_kd_tree(self):
        # params = KDTreeParams(max_leaf_dimension=5.0, max_leaf_size=1)
        raise NotImplementedError()

    def build_crosswalk_polygon_kd_tree(self):
        # params = KDTreeParams(max_leaf_dimension=5.0, max_leaf_size=1)
        raise NotImplementedError()

    def build_signal_segment_kd_tree(self):
        # params = KDTreeParams(max_leaf_dimension=5.0, max_leaf_size=4)
        raise NotImplementedError()

    def build_stop_sign_segment_kd_tree(self):
        # params = KDTreeParams(max_leaf_dimension=5.0, max_leaf_size=4)
        raise NotImplementedError()

    def get_lane_coord_and_heading(self, lane_id: str, s: float) -> Tuple[Point, float]:
        return self.__get_lane_coord_and_heading(lane_id, s)

    @lru_cache(maxsize=20)
    def __get_lane_coord_and_heading(
        self, lane_id: str, s: float
    ) -> Tuple[Point, float]:
        assert (
            lane_id in self.lane_table.keys()
        ), f"lane_id {repr(lane_id)} does not exist"
        assert self.get_lane_by_id(lane_id).length > s

        cv = self.get_lane_by_id(lane_id).central_curve
        cv_points = cv.segment[0].line_segment

        lst = LineString([[x.x, x.y] for x in cv_points.point])
        ip = lst.interpolate(s)

        segments = list(map(LineString, zip(lst.coords[:-1], lst.coords[1:])))
        segments.sort(key=lambda x: ip.distance(x))
        line = segments[0]
        x1, x2 = line.xy[0]
        y1, y2 = line.xy[1]

        return Point(ip.x, ip.y), atan2(y2 - y1, x2 - x1)

    def get_pose_with_regard_to_lane(self, point: Point) -> float:
        return self.__get_pose_with_regard_to_lane(point)

    @lru_cache(maxsize=20)
    def __get_pose_with_regard_to_lane(self, point: Point) -> float:
        obj = self.lane_kdtree.get_nearest_object(point)
        x1, x2 = obj.xy[0]
        y1, y2 = obj.xy[1]
        return atan2(y2 - y1, x2 - x1)

    def get_nearest_lane(self, point: Point) -> str:
        return self.__get_nearest_lane(point)

    @lru_cache(maxsize=20)
    def __get_nearest_lane(self, point: Point) -> str:
        obj = self.lane_kdtree.get_nearest_object(point)
        return self.lane_boxes[obj].lane_id

    def get_nearest_lanes_with_heading(self, point: Point, heading: float) -> List[str]:
        return self.__get_nearest_lanes_with_heading(point, heading)

    @lru_cache(maxsize=20)
    def __get_nearest_lanes_with_heading(
        self, point: Point, heading: float
    ) -> List[str]:
        objs = list(self.lane_kdtree.get_objects(point, 3))
        if len(objs) == 0:
            return []

        filtered_objs = list()
        for i in range(len(objs)):
            x1, x2 = objs[i].xy[0]
            y1, y2 = objs[i].xy[1]
            theta = atan2(y2 - y1, x2 - x1)
            theta_diff = abs(heading - theta)
            unsigned_diff = min(theta_diff, 2 * pi - theta_diff)
            if unsigned_diff < self.kMaxHeadingDiff:
                filtered_objs.append((objs[i], theta, unsigned_diff))

        if len(filtered_objs) == 0:
            return list()

        filtered_objs.sort(key=lambda x: (x[0].distance(point), x[2]))
        result = list()
        for obj in filtered_objs:
            if self.lane_boxes[obj[0]].lane_id not in result:
                result.append(self.lane_boxes[obj[0]].lane_id)
        return result
