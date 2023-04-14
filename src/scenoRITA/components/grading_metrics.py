from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass(slots=True)
class Violation:
    type: str
    features: Dict[str, float]


@dataclass(slots=True)
class GradingResult:
    scenario_id: str
    fitnesses: Dict[int, Tuple[float, ...]]
    violations: List[Violation]


def grade_scenario(scenario_id: str, scenario: Path) -> GradingResult:
    # TODO: Implement this function.
    raise NotImplementedError()
