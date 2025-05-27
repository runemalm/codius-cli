from domain.model.session import Session
from graph.graph import build_graph
from infrastructure.repository.session_repository import SessionRepository

_repo = SessionRepository()


def run_graph(session: Session, user_input: str) -> str:

    # Update state and history with user input
    session.state.user_input = user_input
    session.append_user_message(user_input)

    # Prepare LangGraph input
    graph_input = {
        "user_input": session.state.user_input,
        "history": [m.__dict__ for m in session.history.recent()],
        "project_metadata": session.state.project_metadata,
        "building_blocks": [bb.__dict__ for bb in session.state.building_blocks],
    }

    # Run LangGraph
    graph = build_graph()
    result = graph.invoke(graph_input)

    # Update session state
    session.state.update_with_graph_result(result)

    # Append assistant response to history
    assistant_message = session.state.final_output or "⚠️ No output from assistant."
    session.append_assistant_message(assistant_message)

    return assistant_message
