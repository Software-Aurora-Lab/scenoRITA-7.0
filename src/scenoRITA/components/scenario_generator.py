import random
from typing import Tuple

import networkx as nx

from apollo.map_service import MapService, PositionEstimate

from ..representation import (
    EgoCar,
    Obstacle,
    ObstacleMotion,
    ObstaclePosition,
    ObstacleType,
    Scenario,
)

ObstacleConstraints = {
    ObstacleType.VEHICLE: {
        "speed": (2.0, 14.0),
        "width": (1.5, 2.5),
        "length": (4.0, 14.5),
        "height": (1.5, 4.7),
    },
    ObstacleType.BICYCLE: {
        "speed": (1.6, 8.3),
        "width": (0.5, 1.0),
        "length": (1.0, 2.5),
        "height": (1.0, 2.5),
    },
    ObstacleType.PEDESTRIAN: {
        "speed": (1.25, 2.9),
        "width": (0.24, 0.67),
        "length": (0.2, 0.45),
        "height": (0.97, 1.87),
    },
}


class ScenarioGenerator:
    def __init__(self, map_service: MapService) -> None:
        self.map_service = map_service

    def generate_obstacle_route(self) -> Tuple[ObstaclePosition, ObstaclePosition]:
        while True:
            initial_lane_id = random.choice(list(self.map_service.lane_table.keys()))
            reachable = nx.shortest_path(
                self.map_service.obs_routing_graph, initial_lane_id
            )
            paths = list(filter(lambda x: len(x) > 1, reachable.values()))
            if len(paths) > 0:
                chosen_path = random.choice(paths)
                initial_central_curve = self.map_service.get_lane_central_curve_by_id(
                    initial_lane_id
                )
                initial_xes, _ = initial_central_curve.xy
                initial_index = random.randint(0, len(initial_xes) - 2)

                final_lane_id = chosen_path[-1]
                final_central_curve = self.map_service.get_lane_central_curve_by_id(
                    final_lane_id
                )
                final_xes, _ = final_central_curve.xy
                final_index = random.randint(0, len(final_xes) - 2)

                return ObstaclePosition(
                    initial_lane_id, initial_index
                ), ObstaclePosition(final_lane_id, final_index)

    def generate_obstacle_type(self) -> ObstacleType:
        return random.choice(
            [ObstacleType.VEHICLE, ObstacleType.PEDESTRIAN, ObstacleType.BICYCLE]
        )

    def generate_obstacle_motion(self) -> ObstacleMotion:
        return random.choice([ObstacleMotion.DYNAMIC, ObstacleMotion.STATIC])

    def generate_obstacle_speed(self, obs_type: ObstacleType) -> float:
        return random.uniform(*ObstacleConstraints[obs_type]["speed"])

    def generate_obstacle_dimensions(
        self, obs_type: ObstacleType
    ) -> Tuple[float, float, float]:
        return (
            random.uniform(*ObstacleConstraints[obs_type]["width"]),
            random.uniform(*ObstacleConstraints[obs_type]["length"]),
            random.uniform(*ObstacleConstraints[obs_type]["height"]),
        )

    def generate_obstacle(self) -> Obstacle:
        obs_type = self.generate_obstacle_type()
        initial, final = self.generate_obstacle_route()
        width, length, height = self.generate_obstacle_dimensions(obs_type)

        result = Obstacle(
            id=random.randint(100000, 999999),
            initial_position=initial,
            final_position=final,
            type=obs_type,
            speed=self.generate_obstacle_speed(obs_type),
            width=width,
            length=length,
            height=height,
            motion=self.generate_obstacle_motion(),
        )

        return result

    def generate_ego_car(self) -> EgoCar:
        lane_ids = list(self.map_service.routing_graph.nodes())
        while True:
            lane_id = random.choice(lane_ids)
            descendants = nx.descendants(self.map_service.routing_graph, lane_id)
            if len(descendants) > 0:
                target_lane_id = random.choice(list(descendants))
                return EgoCar(
                    PositionEstimate(lane_id, 1.0),  # at the end of the lane
                    PositionEstimate(
                        target_lane_id,
                        float(int(self.map_service.get_lane_by_id(lane_id).length)),
                    ),
                )
            lane_ids.remove(lane_id)

    def generate_scenario(self, min_obs: int, max_obs: int) -> Scenario:
        num_obs = random.randint(min_obs, max_obs)
        return Scenario(
            ego_car=self.generate_ego_car(),
            obstacles=[self.generate_obstacle() for _ in range(num_obs)],
        )
