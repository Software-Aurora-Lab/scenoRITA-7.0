"""modules/common/math/aaboxkdtree2d.h"""

from enum import Enum, auto
from typing import List, Optional, Tuple

from shapely.geometry import Point, Polygon, box
from shapely.geometry.base import BaseGeometry

from .kdtree_params import KDTreeParams


class Partition(Enum):
    PARTITION_X = auto()
    PARTITION_Y = auto()


class KDTreeNode:
    kMathEpsilon: float = 1e-10

    num_objects: int
    objects_sorted_by_min_: List[BaseGeometry]
    objects_sorted_by_max_: List[BaseGeometry]
    objects_sorted_by_min_bound_: List[float]
    objects_sorted_by_max_bound_: List[float]
    depth_: int

    min_x_: float
    max_x_: float
    min_y_: float
    max_y_: float
    mid_x_: float
    mid_y_: float

    partition_: Partition
    partition_position_: float

    left_subnode_: Optional["KDTreeNode"]
    right_subnode_: Optional["KDTreeNode"]

    def __init__(
        self, objects: List[BaseGeometry], params: KDTreeParams, depth: int
    ) -> None:
        self.depth_ = depth
        assert len(objects) > 0

        self.num_objects = 0
        self.objects_sorted_by_min_ = list()
        self.objects_sorted_by_max_ = list()
        self.objects_sorted_by_min_bound_ = list()
        self.objects_sorted_by_max_bound_ = list()
        self.min_x_ = 0.0
        self.max_x_ = 0.0
        self.min_y_ = 0.0
        self.max_y_ = 0.0
        self.mid_x_ = 0.0
        self.mid_y_ = 0.0

        self.partition_ = Partition.PARTITION_X
        self.partition_position_ = 0.0

        self.left_subnode_ = None
        self.right_subnode_ = None

        self.compute_boundary(objects)
        self.compute_partition()

        if self.split_to_sub_nodes(objects, params):
            lobjects, robjects = self.partition_objects(objects)
            if len(lobjects) > 0:
                self.left_subnode_ = KDTreeNode(lobjects, params, depth + 1)
            if len(robjects) > 0:
                self.right_subnode_ = KDTreeNode(robjects, params, depth + 1)
        else:
            self.init_objects(objects)

    def get_nearest_object(self, point: Point) -> Optional[BaseGeometry]:
        min_distance_sqr = [float("inf")]
        nearest_obj = [None]
        self.__get_nearest_object(point, min_distance_sqr, nearest_obj)
        return nearest_obj[0]

    def __get_nearest_object(
        self,
        point: Point,
        min_distance_sqr: List[float],
        nearest_obj: List[BaseGeometry],
    ) -> BaseGeometry:
        if (
            self.lower_distance_square_to_point(point)
            >= min_distance_sqr[0] - self.kMathEpsilon
        ):
            return
        pvalue = point.x if self.partition_ == Partition.PARTITION_X else point.y
        search_left_first = pvalue < self.partition_position_
        if search_left_first:
            if self.left_subnode_ is not None:
                self.left_subnode_.__get_nearest_object(
                    point, min_distance_sqr, nearest_obj
                )
        else:
            if self.right_subnode_ is not None:
                self.right_subnode_.__get_nearest_object(
                    point, min_distance_sqr, nearest_obj
                )
        if min_distance_sqr[0] <= self.kMathEpsilon:
            return

        if search_left_first:
            for i in range(self.num_objects):
                bound = self.objects_sorted_by_min_bound_[i]
                if bound > pvalue and (bound - pvalue) ** 2 > min_distance_sqr[0]:
                    break
                obj = self.objects_sorted_by_min_[i]
                distance_sqr = obj.distance(point) ** 2
                if distance_sqr < min_distance_sqr[0]:
                    min_distance_sqr[0] = distance_sqr
                    nearest_obj[0] = obj
        else:
            for i in range(self.num_objects):
                bound = self.objects_sorted_by_max_bound_[i]
                if bound < pvalue and (bound - pvalue) ** 2 > min_distance_sqr[0]:
                    break
                obj = self.objects_sorted_by_max_[i]
                distance_sqr = obj.distance(point) ** 2
                if distance_sqr < min_distance_sqr[0]:
                    min_distance_sqr[0] = distance_sqr
                    nearest_obj[0] = obj
        if min_distance_sqr[0] <= self.kMathEpsilon:
            return

        if search_left_first:
            if self.right_subnode_ is not None:
                self.right_subnode_.__get_nearest_object(
                    point, min_distance_sqr, nearest_obj
                )
        else:
            if self.left_subnode_ is not None:
                self.left_subnode_.__get_nearest_object(
                    point, min_distance_sqr, nearest_obj
                )

    def get_all_objects(self) -> List[BaseGeometry]:
        result = list(self.objects_sorted_by_min_)
        if self.left_subnode_ is not None:
            result += self.left_subnode_.get_all_objects()
        if self.right_subnode_ is not None:
            result += self.right_subnode_.get_all_objects()
        return result

    def get_objects(self, point: Point, distance: float) -> List[BaseGeometry]:
        result: List[BaseGeometry] = list()
        self.__get_objects(point, distance, distance**2, result)
        return result

    def __get_objects(
        self,
        point: Point,
        distance: float,
        distance_sqr: float,
        result: List[BaseGeometry],
    ):
        if self.lower_distance_square_to_point(point) > distance_sqr:
            return
        if self.upper_distance_square_to_point(point) <= distance_sqr:
            for obj in self.get_all_objects():
                result.append(obj)
            return
        pvalue = point.x if self.partition_ == Partition.PARTITION_X else point.y
        if pvalue < self.partition_position_:
            limit = pvalue + distance
            for i in range(self.num_objects):
                if self.objects_sorted_by_min_bound_[i] > limit:
                    break
                obj = self.objects_sorted_by_min_[i]
                if obj.distance(point) ** 2 <= distance_sqr:
                    result.append(obj)
        else:
            limit = pvalue - distance
            for i in range(self.num_objects):
                if self.objects_sorted_by_max_bound_[i] < limit:
                    break
                obj = self.objects_sorted_by_max_[i]
                if obj.distance(point) ** 2 <= distance_sqr:
                    result.append(obj)

        if self.left_subnode_ is not None:
            self.left_subnode_.__get_objects(point, distance, distance_sqr, result)
        if self.right_subnode_ is not None:
            self.right_subnode_.__get_objects(point, distance, distance_sqr, result)

    def get_bounding_box(self) -> Polygon:
        return box(self.min_x_, self.min_y_, self.max_x_, self.max_y_)

    def compute_boundary(self, objects: List[BaseGeometry]) -> None:
        self.min_x_ = float("inf")
        self.min_y_ = float("inf")
        self.max_x_ = float("-inf")
        self.max_y_ = float("-inf")
        for object in objects:
            minx, miny, maxx, maxy = object.bounds
            self.min_x_ = min(minx, self.min_x_)
            self.max_x_ = max(maxx, self.max_x_)
            self.min_y_ = min(miny, self.min_y_)
            self.max_y_ = max(maxy, self.max_y_)

        self.mid_x_ = (self.min_x_ + self.max_x_) / 2.0
        self.mid_y_ = (self.min_y_ + self.max_y_) / 2.0

        assert not any(
            x == float("inf") or x == float("-inf")
            for x in [self.min_x_, self.max_x_, self.min_y_, self.max_y_]
        ), "the provided object box size is infinity"

    def compute_partition(self) -> None:
        if self.max_x_ - self.min_x_ >= self.max_y_ - self.min_y_:
            self.partition_ = Partition.PARTITION_X
            self.partition_position_ = (self.min_x_ + self.max_x_) / 2.0
        else:
            self.partition_ = Partition.PARTITION_Y
            self.partition_position_ = (self.min_y_ + self.max_y_) / 2.0

    def split_to_sub_nodes(
        self, objects: List[BaseGeometry], params: KDTreeParams
    ) -> bool:
        if params.max_depth >= 0 and self.depth_ >= params.max_depth:
            return False
        if len(objects) <= max(1, params.max_leaf_size):
            return False
        if (
            params.max_leaf_dimension > 0.0
            and max(self.max_x_ - self.min_x_, self.max_y_ - self.min_y_)
            <= params.max_leaf_dimension
        ):
            return False
        return True

    def partition_objects(
        self, objects: List[BaseGeometry]
    ) -> Tuple[List[BaseGeometry], List[BaseGeometry]]:
        l_subnode_objects = list()
        r_subnode_objects = list()
        other_objects = list()

        for obj in objects:
            minx, miny, maxx, maxy = obj.bounds

            if self.partition_ == Partition.PARTITION_X:
                _max, _min = maxx, minx
            else:
                _max, _min = maxy, miny

            if _max <= self.partition_position_:
                l_subnode_objects.append(obj)
            elif _min >= self.partition_position_:
                r_subnode_objects.append(obj)
            else:
                other_objects.append(obj)

        self.init_objects(other_objects)
        return l_subnode_objects, r_subnode_objects

    def init_objects(self, objects: List[BaseGeometry]):
        self.num_objects = len(objects)
        self.objects_sorted_by_min_ = list(objects)
        self.objects_sorted_by_max_ = list(objects)
        self.objects_sorted_by_min_.sort(
            key=lambda x: x.bounds[0]
            if self.partition_ == Partition.PARTITION_X
            else x.bounds[1]
        )
        self.objects_sorted_by_max_.sort(
            key=lambda x: x.bounds[2]
            if self.partition_ == Partition.PARTITION_X
            else x.bounds[3],
            reverse=True,
        )
        self.objects_sorted_by_min_bound_ = list()
        for obj in self.objects_sorted_by_min_:
            minx, miny, maxx, maxy = obj.bounds
            self.objects_sorted_by_min_bound_.append(
                minx if self.partition_ == Partition.PARTITION_X else miny
            )
        self.objects_sorted_by_max_bound_ = list()
        for obj in self.objects_sorted_by_max_:
            minx, miny, maxx, maxy = obj.bounds
            self.objects_sorted_by_max_bound_.append(
                maxx if self.partition_ == Partition.PARTITION_X else maxy
            )

    def lower_distance_square_to_point(self, p: Point):
        dx = 0.0
        if p.x < self.min_x_:
            dx = self.min_x_ - p.x
        elif p.x > self.max_x_:
            dx = p.x - self.max_x_
        dy = 0.0
        if p.y < self.min_y_:
            dy = self.min_y_ - p.y
        elif p.y > self.max_y_:
            dy = p.y - self.max_y_
        return dx * dx + dy * dy

    def upper_distance_square_to_point(self, p: Point):
        dx = p.x - self.min_x_ if p.x > self.mid_x_ else p.x - self.max_x_
        dy = p.y - self.min_y_ if p.y > self.mid_y_ else p.y - self.max_y_
        return dx * dx + dy * dy
