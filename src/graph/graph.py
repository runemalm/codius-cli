from langgraph.graph import StateGraph, END

from graph.graph_state import GraphState
from graph.nodes.abort import abort
from graph.nodes.apply_changes import apply_changes
from graph.nodes.extract_building_blocks import extract_building_blocks
from graph.nodes.extract_project_metadata import extract_project_metadata
from graph.nodes.extract_relevant_sources import extract_relevant_sources
from graph.nodes.generate_code import generate_code
from graph.nodes.handle_intent_error import handle_intent_error
from graph.nodes.handle_unclear_intent import handle_unclear_intent
from graph.nodes.plan_changes.plan_all_with_llm import plan_all_with_llm
from graph.nodes.plan_changes.plan_changes import plan_changes
from graph.nodes.revise_intent import revise_intent
from graph.routers.approval_router import route_by_user_approval

from graph.nodes.distill_intent import distill_intent
from graph.nodes.preview import preview
from graph.routers.intent_router import route_by_intent


def build_graph():
    graph = StateGraph(state_schema=GraphState)

    # Add nodes
    graph.add_node("DistillIntent", distill_intent)
    graph.add_node("HandleUnclearIntent", handle_unclear_intent)
    graph.add_node("HandleIntentError", handle_intent_error)
    graph.add_node("ExtractProjectMetadata", extract_project_metadata)
    graph.add_node("ExtractBuildingBlocks", extract_building_blocks)
    graph.add_node("ExtractRelevantSources", extract_relevant_sources)
    graph.add_node("PlanChanges", plan_changes)
    graph.add_node("PlanAllWithLlm", plan_all_with_llm)
    graph.add_node("ReviseIntent", revise_intent)
    graph.add_node("GenerateCode", generate_code)
    graph.add_node("Preview", preview)
    graph.add_node("ApplyChanges", apply_changes)
    graph.add_node("Abort", abort)

    # Routers
    graph.add_conditional_edges("DistillIntent", route_by_intent, {
        "valid": "ExtractProjectMetadata",
        "unclear": "HandleUnclearIntent",
        "error": "HandleIntentError"
    })
    graph.add_conditional_edges("Preview", route_by_user_approval, {
        "apply": "ApplyChanges",
        "abort": "Abort",
        "revise": "ReviseIntent"
    })

    # Graph flow
    graph.set_entry_point("DistillIntent")
    graph.add_edge("ExtractProjectMetadata", "ExtractBuildingBlocks")
    graph.add_edge("ExtractBuildingBlocks", "ExtractRelevantSources")
    graph.add_edge("ExtractRelevantSources", "PlanAllWithLlm")
    graph.add_edge("PlanAllWithLlm", "GenerateCode")
    graph.add_edge("GenerateCode", "Preview")
    graph.add_edge("ReviseIntent", "PlanAllWithLlm")
    graph.add_edge("ApplyChanges", END)
    graph.add_edge("Abort", END)

    return graph.compile()
