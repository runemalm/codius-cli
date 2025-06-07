from dataclasses import dataclass

from domain.model.plan_steps.plan_step_base import PlanStepBase
from domain.model.plan_steps.plan_step_type import PlanStepType


@dataclass
class DeleteFileStep(PlanStepBase):
    def __init__(self, path: str, description: str):
        super().__init__(type=PlanStepType.DELETE_FILE, path=path, description=description)
