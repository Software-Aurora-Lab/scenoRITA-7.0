from copy import deepcopy
from typing import List, Tuple

from apollo.map_service import MapService

from .components.scenario_generator import ScenarioGenerator, ObstacleConstraints
from .representation import Obstacle, Scenario
import random

class GeneticOperators:
    def __init__(self, map_service: MapService) -> None:
        self.map_service = map_service
        self.generator = ScenarioGenerator(map_service)

    def get_offsprings(self, parents: List[Obstacle]) -> List[Obstacle]:
        result: List[Obstacle] = list()
        for p in parents:
            result.append(self.mutate(p))
        return result
    
    def _validate_obstacle(self, obstacle: Obstacle) -> None:
        """
        Validates an obstacle's constraints.
        Corrects the obstacle in place if necessary.
        :param obstacle: Obstacle to validate.
        """
        for attribute in ['speed', 'width', 'length', 'height']:
            min_value, max_value = ObstacleConstraints[obstacle.type][attribute]
            current_value = obstacle.__getattribute__(attribute)
            if current_value < min_value or current_value > max_value:
                obstacle.__setattr__(attribute, random.uniform(min_value, max_value))

    def crossover(self, lhs: Obstacle, rhs: Obstacle) -> None:
        """
        Perform crossover between two obstacles.
        Mutates the obstacles in place.
        :param lhs: First obstacle.
        :param rhs: Second obstacle.
        """
        return lhs, rhs

    def mutate(self, obstacle: Obstacle) -> None:
        """
        Perform mutation on an obstacle.
        Mutates the obstacle in place.
        :param obstacle: Obstacle to mutate.
        """
        mut_index = random.randint(0, 6)
        nw, nl, nh = self.generator.generate_obstacle_dimensions(obstacle.type)
        if mut_index == 0:
            init, final = self.generator.generate_obstacle_route()
            obstacle.initial_position = init
            obstacle.final_position = final
        elif mut_index == 1:
            obstacle.type = self.generator.generate_obstacle_type()
        elif mut_index == 2:
            obstacle.speed = self.generator.generate_obstacle_speed(obstacle.type)
        elif mut_index == 3:
            obstacle.width = nw
        elif mut_index == 4:
            obstacle.length = nl
        elif mut_index == 5:
            obstacle.height = nh
        else:
            obstacle.motion = self.generator.generate_obstacle_motion()
    
        self._validate_obstacle(obstacle)

    def select(self, obstacles: List[Obstacle]) -> List[Obstacle]:
        """
        Selects a subset of obstacles from a population.
        :param obstacles: A population of obstacles.
        :return: Selected obstacles.
        """
        return obstacles

    def evaluate_scenarios(self, scenarios: List[Scenario]) -> List[float]:
        return [0.0 for _ in scenarios]
