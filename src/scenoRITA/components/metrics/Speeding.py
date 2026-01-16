import math
from dataclasses import dataclass
from datetime import datetime
from itertools import groupby
from typing import Any, List

from shapely.geometry import Point

from apollo.map_service import MapService

from .BaseMetric import BaseMetric
from .Violation import Violation


@dataclass
class SpeedingTrace:
    t: float
    is_over_speed_limit: bool
    ego_x: float = 0.0
    ego_y: float = 0.0
    ego_theta: float = 0.0
    ego_speed: float = 0.0
    lane_id: str = ""
    lane_speed_limit: float = 0.0


class Speeding(BaseMetric):
    MINIMUM_DURATION = 0.0

    def __init__(self, topics: List[str], map_service: MapService) -> None:
        super().__init__(topics, map_service)
        self.speeding_trace: List[SpeedingTrace] = list()
        self.sorted_lane_ids = sorted(map_service.get_lanes(None))
        self.obs_fitness = float("inf")

    def on_new_message(self, topic: str, msg: Any, t: float) -> None:
        if not self.should_process(t):
            return
        ego_x = msg.pose.position.x
        ego_y = msg.pose.position.y
        ego_theta = msg.pose.heading
        ego_vx = msg.pose.linear_velocity.x
        ego_vy = msg.pose.linear_velocity.y
        ego_speed = math.sqrt(ego_vx**2 + ego_vy**2)
        ego_point = Point(ego_x, ego_y)
        ego_lanes = self.map_service.get_nearest_lanes_with_heading(ego_point, ego_theta)
        
        if not ego_lanes:
            self.speeding_trace.append(SpeedingTrace(t, False))
            return
        
        lane_speed_limits = [
            self.map_service.get_lane_by_id(lane_id).speed_limit
            for lane_id in ego_lanes
            if self.map_service.get_lane_by_id(lane_id).speed_limit > 0.0
        ]
        
        if not lane_speed_limits:
            self.speeding_trace.append(SpeedingTrace(t, False))
            return
        
        current_lane_speed = max(lane_speed_limits)

        self.obs_fitness = min(self.obs_fitness, current_lane_speed - ego_speed)

        if ego_speed > current_lane_speed * 1.1:
            # violation occurred
            self.speeding_trace.append(
                SpeedingTrace(
                    t,  # time
                    True,  # is_over_speed_limit
                    ego_x,  # ego_x
                    ego_y,  # ego_y
                    ego_theta,  # ego_theta
                    ego_speed,  # ego_speed
                    current_lane,  # lane_id
                    current_lane_speed,  # lane_speed_limit
                )
            )
        else:
            self.speeding_trace.append(SpeedingTrace(t, False))

    def get_result(self) -> List[Violation]:
        result: List[Violation] = list()
        for k, iv in groupby(
            self.speeding_trace, key=lambda x: (x.is_over_speed_limit, x.lane_id)
        ):
            if not k[0]:
                continue
            # violation occurred
            v: List[SpeedingTrace] = list(iv)
            violation_start = datetime.fromtimestamp(v[0].t / 1e9)
            violation_end = datetime.fromtimestamp(v[-1].t / 1e9)
            duration = (violation_end - violation_start).total_seconds()
            if duration >= Speeding.MINIMUM_DURATION:
                # violation is long enough
                result.append(
                    Violation(
                        "Speeding",
                        {
                            "ego_x": v[0].ego_x,
                            "ego_y": v[0].ego_y,
                            "ego_theta": v[0].ego_theta,
                            "ego_speed": v[0].ego_speed,
                            "lane_id": self.sorted_lane_ids.index(v[0].lane_id),
                            "lane_speed_limit": v[0].lane_speed_limit,
                            "duration": duration,
                        },
                    )
                )
                break
        return result

    def get_fitness(self) -> float:
        return self.obs_fitness
