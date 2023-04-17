import math
from dataclasses import dataclass
from datetime import datetime
from itertools import groupby
from typing import Any, List

from apollo.map_service import MapService

from .BaseMetric import BaseMetric
from .Violation import Violation


@dataclass(slots=True)
class FastAccelTrace:
    t: float
    violates: bool = False
    ego_x: float = 0.0
    ego_y: float = 0.0
    ego_theta: float = 0.0
    ego_speed: float = 0.0
    ego_accel: float = 0.0


class FastAccel(BaseMetric):
    MINIMUM_DURATION = 1.0
    THRESHOLD = 4.0

    def __init__(self, topics: List[str], map_service: MapService) -> None:
        super().__init__(topics, map_service)
        self.traces: List[FastAccelTrace] = list()
        self.fitness = 0.0

    def on_new_message(self, topic: str, msg: Any, t: float) -> None:
        ego_x = msg.pose.position.x
        ego_y = msg.pose.position.y
        ego_theta = msg.pose.heading

        ego_vx = msg.pose.linear_velocity.x
        ego_vy = msg.pose.linear_velocity.y
        ego_speed = math.sqrt(ego_vx**2 + ego_vy**2)

        ego_ax = msg.pose.linear_acceleration.x
        ego_ay = msg.pose.linear_acceleration.y
        ego_acceleration = math.sqrt(ego_ax**2 + ego_ay**2)

        projection = ego_vx * ego_ax + ego_vy * ego_ay

        if projection < 0:
            ego_acceleration = -ego_acceleration

        self.fitness = max(self.fitness, ego_acceleration)

        if ego_acceleration <= FastAccel.THRESHOLD:
            self.traces.append(FastAccelTrace(t, False))
        else:
            self.traces.append(
                FastAccelTrace(
                    t, True, ego_x, ego_y, ego_theta, ego_speed, ego_acceleration
                )
            )

    def get_fitness(self) -> float:
        return self.fitness

    def get_result(self) -> List[Violation]:
        results: List[Violation] = list()

        for k, iv in groupby(self.traces, lambda x: x.violates):
            if not k:
                # does not violate
                continue

            v: List[FastAccelTrace] = list(iv)
            violation_start = datetime.fromtimestamp(v[0].t / 1e9)
            violation_end = datetime.fromtimestamp(v[-1].t / 1e9)
            duration = (violation_end - violation_start).total_seconds()

            if duration > FastAccel.MINIMUM_DURATION:
                results.append(
                    Violation(
                        "FastAccel",
                        {
                            "ego_x": v[0].ego_x,
                            "ego_y": v[0].ego_y,
                            "ego_theta": v[0].ego_theta,
                            "ego_speed": v[0].ego_speed,
                            "ego_accel": v[0].ego_accel,
                            "duration": duration,
                        },
                    )
                )

        return results
