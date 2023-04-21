import random
from copy import deepcopy
from typing import List, Set

from deap.tools import selNSGA2
from shapely.geometry import Point

from apollo.map_service import MapService

from .components.scenario_generator import ObstacleConstraints, ScenarioGenerator
from .representation import Obstacle, ObstacleMotion, Scenario


class GeneticOperators:
    def __init__(
        self,
        map_service: MapService,
        mut_pb: float,
        cx_pb: float,
        add_pb: float,
        del_pb: float,
        replace_pb: float,
        min_obs: int,
        max_obs: int,
        dry_run: bool,
    ) -> None:
        self.map_service = map_service
        self.generator = ScenarioGenerator(map_service)
        self.mut_pb = mut_pb
        self.cx_pb = cx_pb
        self.add_pb = add_pb
        self.del_pb = del_pb
        self.replace_pb = replace_pb
        self.min_obs = min_obs
        self.max_obs = max_obs
        self.dry_run = dry_run

    def get_offsprings(self, scenarios: List[Scenario]) -> List[Scenario]:
        result: List[Scenario] = list()
        for scenario in scenarios:
            next_generation_id = scenario.generation_id + 1
            scenario_id = scenario.scenario_id
            ego = deepcopy(scenario.ego_car)
            obstacles = [deepcopy(x) for x in scenario.obstacles]
            for obs in obstacles:
                del obs.fitness.values

            if random.random() < self.replace_pb:
                # replace ego car
                ego = self.generator.generate_ego_car()
            else:
                # apply crossover to obstacles
                for o1, o2 in zip(obstacles[::2], obstacles[1::2]):
                    if random.random() < self.cx_pb:
                        self.crossover(o1, o2)
                # apply mutation to obstacles
                for mutant in obstacles:
                    if random.random() < self.mut_pb:
                        self.mutate(mutant)
                # add obstacles
                if len(obstacles) > self.min_obs and random.random() < self.del_pb:
                    del obstacles[random.randint(0, len(obstacles) - 1)]
                if len(obstacles) < self.max_obs and random.random() < self.add_pb:
                    obstacles.append(self.generator.generate_obstacle(ego))

            # validate scenario
            obs_size = len(obstacles)
            obs_routes: Set[str] = set()
            obs_static: Set[Point] = set()
            for obs in list(obstacles):
                # validate obstacles far enough from ego car
                ego_point, _ = self.map_service.get_lane_coord_and_heading(
                    ego.initial_position.lane_id, ego.initial_position.s
                )
                obs_lane = obs.initial_position.lane_id
                obs_index = obs.initial_position.index
                obs_xes, obs_yes = self.map_service.get_lane_central_curve_by_id(
                    obs_lane
                ).xy
                obs_point = Point(obs_xes[obs_index], obs_yes[obs_index])

                if ego_point.distance(obs_point) < max(obs.length, 5):
                    # obstacle's initial position is too close to the ego car
                    obstacles.remove(obs)
                    continue

                # validate obstacles that share same lane
                obs_route = (
                    f"{obs.initial_position.lane_id}-{obs.initial_position.index}-"
                    f"{obs.final_position.lane_id}-{obs.final_position.index}"
                )
                obs_initial_lane = obs.initial_position.lane_id
                lst = self.map_service.get_lane_central_curve_by_id(obs_initial_lane)
                obs_xes, obs_yes = lst.xy
                obs_initial_x, obs_initial_y = (
                    obs_xes[obs.initial_position.index],
                    obs_yes[obs.initial_position.index],
                )
                obs_initial_point = Point(obs_initial_x, obs_initial_y)

                if obs.motion == ObstacleMotion.STATIC:
                    for obs_i in obs_static:
                        if obs_initial_point.distance(obs_i) < max(obs.length, 5):
                            # obstacle's initial position is
                            #   too close to another static obstacle
                            obstacles.remove(obs)
                            break
                    else:
                        obs_static.add(obs_initial_point)
                elif obs.motion == ObstacleMotion.DYNAMIC:
                    if obs_route in obs_routes:
                        # obstacle's route overlaps with another obstacle
                        obstacles.remove(obs)
                    else:
                        obs_routes.add(obs_route)

            # generate new obstacles if necessary
            while len(obstacles) < obs_size:
                obstacles.append(self.generator.generate_obstacle(ego))

            result.append(Scenario(next_generation_id, scenario_id, ego, obstacles))

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
        For each scenario, select the best obstacles from the previous and current.
        :param prev_scenarios: Previous scenarios.
        :param curr_scenarios: Current scenarios.
        :return: scenarios for next generation.
        """
        result: List[Scenario] = list()
        for prev, curr in zip(prev_scenarios, curr_scenarios):
            if prev.ego_car == curr.ego_car:
                # select obstacles
                result.append(
                    Scenario(
                        generation_id=curr.generation_id,
                        scenario_id=curr.scenario_id,
                        ego_car=curr.ego_car,
                        obstacles=selNSGA2(
                            prev.obstacles + curr.obstacles, len(curr.obstacles), "log"
                        ),
                    )
                )
            else:
                # ego car changed, no selection
                result.append(curr)
        return result
