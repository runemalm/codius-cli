from dataclasses import dataclass
from typing import Dict

from domain.model.plan_steps.delete_file_step import PlanStepType
from domain.model.plan_steps.plan_step_base import PlanStepBase


@dataclass
class CreateFileStep(PlanStepBase):
    template: str
    context: Dict[str, object]

    def __init__(self, path: str, description: str, template: str, context: dict):
        super().__init__(type=PlanStepType.CREATE_FILE, path=path, description=description)
        self.template = template
        self.context = context
