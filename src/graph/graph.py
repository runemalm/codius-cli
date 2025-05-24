from langgraph.graph import StateGraph, END

from graph.graph_state import GraphState
from graph.nodes.abort import abort
from graph.nodes.apply_changes import apply_changes
from graph.nodes.generate_code import generate_code
from graph.nodes.plan_changes import plan_changes
from graph.routers.approval_router import route_by_user_approval

from graph.nodes.distill_intent import distill_intent
from graph.nodes.preview import preview

def build_graph():
    graph = StateGraph(state_schema=GraphState)

    # Add nodes
    graph.add_node("DistillIntent", distill_intent)
    graph.add_node("PlanChanges", plan_changes)
    graph.add_node("GenerateCode", generate_code)
    graph.add_node("Preview", preview)
    graph.add_node("ApplyChanges", apply_changes)
    graph.add_node("Abort", abort)

    # Add router node
    graph.add_conditional_edges("Preview", route_by_user_approval, {
        "apply": "ApplyChanges",
        "abort": "Abort"
    })

    # Graph flow
    graph.set_entry_point("DistillIntent")
    graph.add_edge("DistillIntent", "PlanChanges")
    graph.add_edge("PlanChanges", "GenerateCode")
    graph.add_edge("GenerateCode", "Preview")
    graph.add_edge("ApplyChanges", END)
    graph.add_edge("Abort", END)

    return graph.compile()
