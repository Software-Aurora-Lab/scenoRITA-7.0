from dataclasses import dataclass
from datetime import datetime
from itertools import groupby
from typing import Any, List, Optional

from shapely.geometry import Point, Polygon

from apollo.map_service import MapService
from apollo.utils import generate_adc_polygon

from .BaseMetric import BaseMetric
from .Violation import Violation


@dataclass
class USLCTrace:
    """A trace of unsafe lane change."""

    t: float
    is_on_boundary: bool = False
    ego_x: float = 0.0
    ego_y: float = 0.0
    ego_theta: float = 0.0
    ego_speed: float = 0.0
    lane_id: str = ""


class UnsafeLaneChange(BaseMetric):
    MINIMUM_DURATION = 5.0

    def __init__(self, topics: List[str], map_service: MapService) -> None:
        super().__init__(topics, map_service)
        self.fitness: Optional[float] = None
        self.traces: List[USLCTrace] = list()
        self.sorted_lane_ids = sorted(map_service.get_lanes(None))

    def on_new_message(self, topic: str, msg: Any, t: float) -> None:
        if not self.should_process(t):
            return

        ego_x = msg.pose.position.x
        ego_y = msg.pose.position.y
        ego_theta = msg.pose.heading
        ego_vx = msg.pose.linear_velocity.x
        ego_vy = msg.pose.linear_velocity.y
        ego_speed = (ego_vx**2 + ego_vy**2) ** 0.5
        ego_point = Point(ego_x, ego_y)
        ego_polygon = generate_adc_polygon(ego_x, ego_y, 0.0, ego_theta)
        ego_p = Polygon(ego_polygon)

        ego_lane = self.map_service.get_nearest_lanes_with_heading(ego_point, ego_theta)
        ego_lane.sort()

        if len(ego_lane) == 0:
            # TODO: ego is not on any lane
            self.traces.append(USLCTrace(t))
            return

        if ego_speed == 0.0:
            self.traces.append(USLCTrace(t))
            return

        for lane_id in ego_lane:
            lboundary, rboundary = self.map_service.get_lane_boundaries_by_id(lane_id)
            if not lboundary.intersects(ego_p) and not rboundary.intersects(ego_p):
                # ego is within lane boundaries of a lane
                self.traces.append(USLCTrace(t))
                return

        self.traces.append(
            USLCTrace(t, True, ego_x, ego_y, ego_theta, ego_speed, ego_lane[0])
        )

    def get_fitness(self) -> float:
        assert self.fitness is not None, "Fitness is not calculated yet."
        return self.fitness

    def get_result(self) -> List[Violation]:
        results: List[Violation] = list()
        self.fitness = 0.0
        for k, iv in groupby(self.traces, lambda x: (x.is_on_boundary, x.lane_id)):
            if not k[0]:
                # ego is not on boundary
                continue

            v: List[USLCTrace] = list(iv)
            violation_start = datetime.fromtimestamp(v[0].t / 1e9)
            violation_end = datetime.fromtimestamp(v[-1].t / 1e9)
            duration = (violation_end - violation_start).total_seconds()

            if self.fitness is None or duration > self.fitness:
                self.fitness = duration

            if duration > self.MINIMUM_DURATION:
                results.append(
                    Violation(
                        "UnsafeLaneChange",
                        {
                            "ego_x": v[0].ego_x,
                            "ego_y": v[0].ego_y,
                            "ego_theta": v[0].ego_theta,
                            "ego_speed": v[0].ego_speed,
                            "lane_id": self.sorted_lane_ids.index(k[1]),
                            "duration": duration,
                        },
                    )
                )

        return results
