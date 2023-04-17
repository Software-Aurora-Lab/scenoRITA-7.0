from collections import defaultdict
from typing import Any, Dict, List, Optional, Set

from shapely.geometry import LineString, Polygon

from apollo.map_service import MapService
from apollo.utils import (
    generate_adc_front_vertices,
    generate_adc_rear_vertices,
    generate_polygon,
)
from modules.common_msgs.localization_msgs.localization_pb2 import LocalizationEstimate
from modules.common_msgs.perception_msgs.perception_obstacle_pb2 import (
    PerceptionObstacles,
)

from .BaseMetric import BaseMetric
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

        # ego_polygon = generate_adc_polygon(ego_x, ego_y, 0.0, ego_theta)
        # ego_p = Polygon(ego_polygon)
        ego_front = generate_adc_front_vertices(ego_x, ego_y, 0.0, ego_theta)
        ego_front_l = LineString(ego_front)
        ego_rear = generate_adc_rear_vertices(ego_x, ego_y, 0.0, ego_theta)
        ego_rear_l = LineString(ego_rear)

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

            if obs_p.distance(ego_rear_l) == 0.0:
                # rear end collision
                self.ignored_obstacles.add(obs.id)
                self.obs_fitness[obs.id] = float("inf")
                continue

            # distance = ego_p.distance(obs_p)
            distance = ego_front_l.distance(obs_p)
            self.obs_fitness[obs.id] = min(distance, self.obs_fitness[obs.id])
            if distance == 0.0 and ego_speed > 0.0:
                # collision ocurred
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
                self.ignored_obstacles.add(obs.id)

    def get_result(self) -> List[Violation]:
        return self.violations

    def get_fitness(self) -> Dict[int, float]:
        return self.obs_fitness
