from dataclasses import dataclass, field
from enum import Enum, auto

from deap import base

from apollo.map_service import PositionEstimate
from modules.common_msgs.perception_msgs.perception_obstacle_pb2 import (
    PerceptionObstacle,
)


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
    ego_car: EgoCar
    obstacles: list[Obstacle]
