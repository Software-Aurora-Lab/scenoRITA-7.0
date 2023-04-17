from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass(slots=True)
class Violation:
    type: str
    features: Dict

    def asdict(self) -> Dict[str, Any]:
        return asdict(self)
