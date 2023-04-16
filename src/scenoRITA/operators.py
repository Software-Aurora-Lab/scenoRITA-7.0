import random
from copy import deepcopy
from typing import List

from apollo.container import ApolloContainer
from apollo.map_service import MapService

from .components.scenario_generator import ObstacleConstraints, ScenarioGenerator
from .representation import Obstacle, ObstacleFitness, Scenario


class GeneticOperators:
    def __init__(self, map_service: MapService, dry_run: bool) -> None:
        self.map_service = map_service
        self.generator = ScenarioGenerator(map_service)
        self.dry_run = dry_run

    def get_offsprings(self, scenarios: List[Scenario]) -> List[Scenario]:
        # TODO: implement offspring generation
        result: List[Scenario] = list()
        for scenario in scenarios:
            obstacle_parents = [deepcopy(x) for x in scenario.obstacles]
            for obs in obstacle_parents:
                del obs.fitness.values
            result.append(
                Scenario(
                    generation_id=scenario.generation_id + 1,
                    scenario_id=scenario.scenario_id,
                    ego_car=scenario.ego_car,
                    obstacles=obstacle_parents,
                )
            )
        return result

    def _validate_obstacle(self, obstacle: Obstacle) -> None:
        """
        Validates an obstacle's constraints.
            Corrects the obstacle in place if necessary.
        :param obstacle: Obstacle to validate.
        """
        for attribute in ["speed", "width", "length", "height"]:
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
        cx_index = random.randint(0, 6)
        if cx_index < 1:
            lhs.initial_position, rhs.initial_position = (
                rhs.initial_position,
                lhs.initial_position,
            )
            lhs.final_position, rhs.final_position = (
                rhs.final_position,
                lhs.final_position,
            )
        if cx_index < 2:
            lhs.type, rhs.type = rhs.type, lhs.type
        if cx_index < 3:
            lhs.speed, rhs.speed = rhs.speed, lhs.speed
        if cx_index < 4:
            lhs.width, rhs.width = rhs.width, lhs.width
        if cx_index < 5:
            lhs.length, rhs.length = rhs.length, lhs.length
        if cx_index < 6:
            lhs.height, rhs.height = rhs.height, lhs.height
        if cx_index < 7:
            lhs.motion, rhs.motion = rhs.motion, lhs.motion

        self._validate_obstacle(lhs)
        self._validate_obstacle(rhs)

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

    def select(
        self, prev_scenarios: List[Scenario], curr_scenarios: List[Scenario]
    ) -> List[Scenario]:
        """
        Selects a subset of obstacles from a population.
        :param prev_scenarios: Previous sub-populations.
        :param curr_scenarios: Current sub-populations.
        :return: Sub-populations for next generation.
        """
        return curr_scenarios

    def evaluate_scenarios(
        self, containers: List[ApolloContainer], scenarios: List[Scenario]
    ) -> None:
        # TODO: implement scenario evaluation
        """
        Evaluates a list of scenarios, assigning a fitness value to each scenario.
            Mutates the scenarios in place.
        :param containers: Apollo containers.
        :param scenarios: Scenarios to evaluate.
        """
        if self.dry_run:
            for scenario in scenarios:
                for obs in scenario.obstacles:
                    obs.fitness.values = tuple(
                        random.random() for _ in range(len(ObstacleFitness.weights))
                    )
