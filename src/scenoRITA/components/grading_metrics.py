import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from cyber_record.record import Record

from apollo.map_service import MapService
from scenoRITA.representation import Scenario

from .metrics import (
    Collision,
    FastAccel,
    HardBraking,
    Speeding,
    UnsafeLaneChange,
    Violation,
)


@dataclass(slots=True)
class GradingResult:
    scenario_id: str
    record: Path
    fitnesses: Dict[int, Tuple[float, ...]]
    violations: List[Violation]


def get_grading_metrics(
    map_service: MapService,
) -> Tuple[Collision, Speeding, UnsafeLaneChange, FastAccel, HardBraking]:
    """Get the grading metrics."""
    loc = "/apollo/localization/pose"
    obs = "/apollo/perception/obstacles"
    return (
        Collision([loc, obs], map_service),
        Speeding([loc], map_service),
        UnsafeLaneChange([loc], map_service),
        FastAccel([loc], map_service),
        HardBraking([loc], map_service),
    )


def grade_scenario(
    scenario: Scenario, record: Path, map_service: MapService
) -> Optional[GradingResult]:
    trial = 0
    while trial < 3:
        try:
            record_file = Record(record, "r")
            metrics = get_grading_metrics(map_service)
            for topic, msg, t in record_file.read_messages():
                for metric in metrics:
                    if topic in metric.topics:
                        metric.on_new_message(topic, msg, t)

            collision, speeding, unsafe_lane_change, fast_accel, hard_braking = metrics

            violations: List[Violation] = list()
            for met in metrics:
                violations.extend(met.get_result())

            collision_fitness = collision.get_fitness()
            fitness: Dict[int, Tuple[float, ...]] = dict()
            for k in collision_fitness:
                fitness[k] = (
                    collision_fitness[k],  # collision
                    speeding.get_fitness(),  # speeding
                    unsafe_lane_change.get_fitness(),  # unsafe lane change
                    fast_accel.get_fitness(),  # fast accel
                    hard_braking.get_fitness(),  # hard braking
                )

            return GradingResult(
                scenario.get_id(),
                record,
                fitness,
                violations,
            )
        except Exception:
            trial += 1
            time.sleep(1)
    return None
