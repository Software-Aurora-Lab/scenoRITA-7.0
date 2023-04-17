from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from apollo.map_service import MapService
from scenoRITA.representation import ObstacleFitness, Scenario


@dataclass(slots=True)
class Violation:
    type: str
    features: Dict[str, float]


@dataclass(slots=True)
class GradingResult:
    scenario_id: str
    fitnesses: Dict[int, Tuple[float, ...]]
    violations: List[Violation]


def grade_scenario(
    scenario: Scenario, record: Path, map_service: MapService
) -> GradingResult:
    fallback_fitness = dict()
    for obs in scenario.obstacles:
        fitness_values = list()
        for weight in ObstacleFitness.weights:
            if weight == 1.0:
                fitness_values.append(float("-inf"))
            else:
                fitness_values.append(float("inf"))
        fallback_fitness[obs.id] = tuple(fitness_values)

    print(fallback_fitness)
    return GradingResult(scenario.get_id(), {}, [])
