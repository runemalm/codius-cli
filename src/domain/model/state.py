from dataclasses import dataclass, field
from typing import Optional

@dataclass
class State:
    user_input: str = ""
    intent: Optional[dict] = None
    plan: Optional[dict] = None
    domain_summary: Optional[str] = None
    generated_files: list[dict] = field(default_factory=list)
    final_output: Optional[str] = None
    status: str = "new"

    def update_with_graph_result(self, result: dict):
        self.intent = result.get("intent")
        self.plan = result.get("plan")
        self.generated_files = result.get("generated_files", [])
        self.final_output = result.get("final_output")
        self.status = result.get("status", "completed")
