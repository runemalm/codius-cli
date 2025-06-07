from abc import ABC
from dataclasses import asdict, dataclass

from domain.model.plan_steps.plan_step_type import PlanStepType


@dataclass
class PlanStepBase(ABC):
    type: PlanStepType
    path: str
    description: str

    def to_dict(self) -> dict:
        return asdict(self)
