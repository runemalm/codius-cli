from langgraph.graph import StateGraph, END

from graph.graph_state import GraphState
from graph.nodes.abort import abort
from graph.nodes.apply_changes import apply_changes
from graph.nodes.enforce_conventions import enforce_conventions
from graph.nodes.extract_building_blocks import extract_building_blocks
from graph.nodes.extract_project_metadata import extract_project_metadata
from graph.nodes.generate_code import generate_code
from graph.nodes.handle_unclear_intent import handle_unclear_intent
from graph.nodes.integrate_changes import integrate_changes
from graph.nodes.plan_changes import plan_changes
from graph.routers.approval_router import route_by_user_approval

from graph.nodes.distill_intent import distill_intent
from graph.nodes.preview import preview
from graph.routers.intent_router import route_by_intent


def build_graph():
    graph = StateGraph(state_schema=GraphState)

    # Add nodes
    graph.add_node("DistillIntent", distill_intent)
    graph.add_node("HandleUnclearIntent", handle_unclear_intent)
    graph.add_node("ExtractProjectMetadata", extract_project_metadata)
    graph.add_node("ExtractBuildingBlocks", extract_building_blocks)
    graph.add_node("EnforceConventions", enforce_conventions)
    graph.add_node("IntegrateChanges", integrate_changes)
    graph.add_node("PlanChanges", plan_changes)
    graph.add_node("GenerateCode", generate_code)
    graph.add_node("Preview", preview)
    graph.add_node("ApplyChanges", apply_changes)
    graph.add_node("Abort", abort)

    # Routers
    graph.add_conditional_edges("DistillIntent", route_by_intent, {
        "valid": "ExtractProjectMetadata",
        "unclear": "HandleUnclearIntent"
    })
    graph.add_conditional_edges("Preview", route_by_user_approval, {
        "apply": "ApplyChanges",
        "abort": "Abort"
    })

    # Graph flow
    graph.set_entry_point("DistillIntent")
    graph.add_edge("ExtractProjectMetadata", "ExtractBuildingBlocks")
    graph.add_edge("ExtractBuildingBlocks", "EnforceConventions")
    graph.add_edge("EnforceConventions", "IntegrateChanges")
    graph.add_edge("IntegrateChanges", "PlanChanges")
    graph.add_edge("PlanChanges", "GenerateCode")
    graph.add_edge("GenerateCode", "Preview")
    graph.add_edge("ApplyChanges", END)
    graph.add_edge("Abort", END)

    return graph.compile()
