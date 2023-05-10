from collections import defaultdict
from typing import Any, Dict, List, Optional, Set

from shapely.geometry import LineString, Point, Polygon

from apollo.map_service import MapService
from apollo.utils import (
    generate_adc_front_vertices,
    generate_adc_polygon,
    generate_adc_rear_vertices,
    generate_polygon,
)
from modules.localization.proto.localization_pb2 import LocalizationEstimate
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacles

from .BaseMetric import BaseMetric
from .OracleInterrupt import OracleInterrupt
from .Violation import Violation


class Collision(BaseMetric):
    def __init__(self, topics: List[str], map_service: MapService) -> None:
        super().__init__(topics, map_service)
        self.ignored_obstacles: Set[int] = set()
        self.obs_fitness: Dict[int, float] = defaultdict(lambda: float("inf"))
        self.last_localization: Optional[LocalizationEstimate] = None
        self.last_perception_obstacles: Optional[PerceptionObstacles] = None
        self.violations: List[Violation] = list()

    def on_new_message(self, topic: str, msg: Any, t: float) -> None:
        if topic == "/apollo/localization/pose":
            self.last_localization = msg
        elif topic == "/apollo/perception/obstacles":
            self.last_perception_obstacles = msg

        if (
            self.last_localization is None
            or self.last_perception_obstacles is None
            or not self.should_process(t)
        ):
            return

        ego_x = self.last_localization.pose.position.x
        ego_y = self.last_localization.pose.position.y
        ego_vx = self.last_localization.pose.linear_velocity.x
        ego_vy = self.last_localization.pose.linear_velocity.y
        ego_speed = (ego_vx**2 + ego_vy**2) ** 0.5
        ego_theta = self.last_localization.pose.heading

        ego_polygon = generate_adc_polygon(ego_x, ego_y, 0.0, ego_theta)
        ego_p = Polygon(ego_polygon)
        ego_front = generate_adc_front_vertices(ego_x, ego_y, 0.0, ego_theta)
        ego_front_l = LineString(ego_front)
        ego_rear = generate_adc_rear_vertices(ego_x, ego_y, 0.0, ego_theta)
        ego_rear_l = LineString(ego_rear)

        collision_detected = False
        for obs in self.last_perception_obstacles.perception_obstacle:
            if obs.id in self.ignored_obstacles:
                continue

            obs_x = obs.position.x
            obs_y = obs.position.y
            obs_theta = obs.theta
            obs_polygon = generate_polygon(
                obs_x, obs_y, 0.0, obs.theta, obs.length, obs.width
            )
            obs_p = Polygon(obs_polygon)
            obs_p_area = obs_p.area

            if obs_p.distance(ego_rear_l) == 0.0:
                # rear end collision
                self.ignored_obstacles.add(obs.id)
                self.obs_fitness[obs.id] = float("inf")
                collision_detected = True
                continue

            # distance = ego_p.distance(obs_p)
            distance = ego_front_l.distance(obs_p)
            self.obs_fitness[obs.id] = min(distance, self.obs_fitness[obs.id])
            if distance == 0.0 and ego_speed > 0.000:
                # front-end collision ocurred

                # check if obs is in lane
                # obs_lane = self.map_service.get_nearest_lanes_with_heading(
                #     Point(obs_x, obs_y), obs_theta
                # )
                obs_lane = self.map_service.get_lanes(Point(obs_x, obs_y), 10)
                obs_in_lane = False
                for lane_id in obs_lane:
                    lboundary, rboundary = self.map_service.get_lane_boundaries_by_id(
                        lane_id
                    )
                    lx, ly = lboundary.xy
                    rx, ry = rboundary.xy
                    x_es = lx + rx[::-1]
                    y_es = ly + ry[::-1]
                    lane_polygon = Polygon([(x, y) for x, y in zip(x_es, y_es)])

                    # if there is no intersection, obs is not in this lane
                    if not lane_polygon.intersects(obs_p):
                        continue

                    # if there is intersection, check if the obs is fully in lane
                    intersection_area = lane_polygon.intersection(obs_p).area
                    if abs(intersection_area - obs_p_area) < 1e-3:
                        obs_in_lane = True
                        break

                # add violation if obs is in lane
                if obs_in_lane:
                    self.violations.append(
                        Violation(
                            "Collision",
                            {
                                "ego_x": ego_x,
                                "ego_y": ego_y,
                                "ego_theta": ego_theta,
                                "ego_speed": ego_speed,
                                "obs_x": obs_x,
                                "obs_y": obs_y,
                                "obs_type": obs.type,
                                "obs_theta": obs_theta,
                                "obs_length": obs.length,
                                "obs_width": obs.width,
                            },
                        )
                    )
                else:
                    self.obs_fitness[obs.id] = float("inf")
                self.ignored_obstacles.add(obs.id)
                collision_detected = True
                continue

            if ego_p.distance(obs_p) == 0.0:
                # other collision
                collision_detected = True
                self.obs_fitness[obs.id] = float("inf")
                continue

        if collision_detected:
            raise OracleInterrupt()

    def get_result(self) -> List[Violation]:
        return self.violations

    def get_fitness(self) -> Dict[int, float]:
        return self.obs_fitness
