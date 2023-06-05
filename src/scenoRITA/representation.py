from dataclasses import dataclass, field
from enum import Enum, auto
from random import randint
from typing import List, Set

from deap import base

from apollo.map_service import PositionEstimate
from modules.perception.proto.perception_obstacle_pb2 import PerceptionObstacle


class ObstacleType(Enum):
    VEHICLE = PerceptionObstacle.VEHICLE
    PEDESTRIAN = PerceptionObstacle.PEDESTRIAN
    BICYCLE = PerceptionObstacle.BICYCLE


class ObstacleMotion(Enum):
    STATIC = auto()
    DYNAMIC = auto()


@dataclass(slots=True)
class ObstaclePosition:
    lane_id: str
    index: int


class ObstacleFitness(base.Fitness):
    # minimize the distance between the ego car and the obstacle
    # minimize difference between speed and limit
    # maximize ego duration on boundary
    # maximize ego car acceleration
    # minimize ego car deceleration
    weights = (-1.0, -1.0, 1.0, 1.0, -1.0)

    @staticmethod
    def get_fallback_fitness() -> tuple[float, ...]:
        result: List[float] = list()
        for w in ObstacleFitness.weights:
            if w == 1.0:
                result.append(float("-inf"))
            else:
                result.append(float("inf"))
        return tuple(result)


@dataclass(slots=True)
class Obstacle:
    id: int
    initial_position: ObstaclePosition
    final_position: ObstaclePosition
    type: ObstacleType
    speed: float
    width: float
    length: float
    height: float
    motion: ObstacleMotion
    fitness: ObstacleFitness = field(default_factory=ObstacleFitness)


@dataclass(slots=True)
class EgoCar:
    initial_position: PositionEstimate
    final_position: PositionEstimate


@dataclass(slots=True)
class Scenario:
    generation_id: int
    scenario_id: int
    ego_car: EgoCar
    obstacles: list[Obstacle]

    def __post_init__(self):
        self.reassign_obs_ids()

    def get_id(self) -> str:
        return f"gen_{self.generation_id}_sce_{self.scenario_id}"

    def reassign_obs_ids(self) -> bool:
        """
        Reassigns obstacle ids to be unique.
        :return: True if ids were reassigned, False otherwise
        """
        current_ids = [obs.id for obs in self.obstacles]
        if len(set(current_ids)) == len(current_ids):
            # all ids are unique
            return False

        ids: Set[int] = set()
        while len(ids) < len(self.obstacles):
            ids.add(randint(10000, 99999))
        for obs, oid in zip(self.obstacles, ids):
            obs.id = oid
        return True
