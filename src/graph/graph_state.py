from typing import Self, TypedDict

from infrastructure.service.code_scanner.model.building_block import BuildingBlock


class GraphState(TypedDict, total=False):
    user_input: str
    intent: dict
    plan: dict
    generated_files: list[dict]
    final_output: str
    approval: str
    session_id: str
    history: list[dict]
    project_metadata: dict
    building_blocks: list[dict]
