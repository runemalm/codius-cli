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
        "domain_summary": session.state.domain_summary,
        "history": [m.__dict__ for m in session.history.recent()]
    }

    # Run LangGraph
    graph = build_graph()
    result = graph.invoke(graph_input)

    # Update session state
    session.state.intent = result.get("intent")
    session.state.plan = result.get("plan")
    session.state.generated_files = result.get("generated_files", [])
    session.state.final_output = result.get("final_output")
    session.state.status = result.get("status", "complete")

    # Append assistant response to history
    assistant_message = session.state.final_output or "⚠️ No output from assistant."
    session.append_assistant_message(assistant_message)

    return assistant_message
