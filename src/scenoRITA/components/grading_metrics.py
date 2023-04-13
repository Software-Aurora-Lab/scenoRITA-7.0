from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(slots=True)
class Violation:
    type: str
    features: Dict[str, float]


def grade_scenario(
    scenario_id: str,
) -> Tuple[Dict[str, Tuple[float, ...]], List[Violation]]:
    return dict(), list()
