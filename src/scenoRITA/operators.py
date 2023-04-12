from typing import List, Tuple

from apollo.map_service import MapService

from .components.scenario_generator import ScenarioGenerator
from .representation import Obstacle, Scenario


class GeneticOperators:
    def __init__(self, map_service: MapService) -> None:
        self.map_service = map_service
        self.generator = ScenarioGenerator(map_service)

    def get_offsprings(self, parents: List[Obstacle]) -> List[Obstacle]:
        result: List[Obstacle] = list()
        for p in parents:
            result.append(self.mutate(p))
        return result

    def crossover(self, lhs: Obstacle, rhs: Obstacle) -> Tuple[Obstacle, Obstacle]:
        return lhs, rhs

    def mutate(self, obstacle: Obstacle) -> Obstacle:
        return obstacle

    def evaluate_scenarios(self, scenarios: List[Scenario]) -> List[float]:
        return [0.0 for _ in scenarios]
