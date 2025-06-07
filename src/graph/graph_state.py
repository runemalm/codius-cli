from typing import Any, Dict, List, TypedDict


class GraphState(TypedDict, total=False):
    user_input: str
    intent: List[Dict[str, Any]]
    plan: List[Dict[str, Any]]
    plan_warnings: List[str]
    generated_files: List[Dict[str, Any]]
    approval: str
    revision_feedback: str
    revision_history: List[Dict[str, Any]]
    revise_mode: bool
    final_output: str
    session_id: str
    history: List[Dict[str, Any]]
    summary: str
    project_metadata: Dict[str, Any]
    building_blocks: List[Dict[str, Any]]
