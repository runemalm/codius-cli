from typing import TypedDict


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
