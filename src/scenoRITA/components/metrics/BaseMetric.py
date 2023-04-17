from abc import ABC, abstractmethod
from typing import Any, Dict, List

from apollo.map_service import MapService

from .Violation import Violation


class BaseMetric(ABC):
    FPS = 24

    def __init__(self, topics: List[str], map_service: MapService) -> None:
        self.topics = topics
        self.last_timestamp: float = 0
        self.map_service = map_service

    def should_process(self, t: float) -> bool:
        if self.last_timestamp is None:
            self.last_timestamp = t
            return True
        if (t - self.last_timestamp) > (1 / BaseMetric.FPS * 1e9):
            self.last_timestamp = t
            return True
        return False

    @abstractmethod
    def on_new_message(self, topic: str, msg: Any, t: float) -> None:
        ...

    @abstractmethod
    def get_result(self) -> List[Violation]:
        ...

    @abstractmethod
    def get_fitness(self) -> Dict[int, float] | float:
        ...
