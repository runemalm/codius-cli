import json

from domain.model.session.session import Session
from domain.services.session_factory import create_session
from infrastructure.repository.session_repository import SessionRepository
from infrastructure.services.llm_service import LlmService

_repo = SessionRepository()


def create_and_activate_session(name: str | None = None):
    session = create_session(name)
    _repo.save(session)
    return session

def get_or_create_active_session() -> Session:
    try:
        return _repo.get_active_session()
    except FileNotFoundError:
        session = create_session()
        _repo.save(session)
        return session

def get_active_session():
    return _repo.get_active_session()

def get_active_session_id() -> str:
    return get_active_session().id

def list_sessions():
    return _repo.get_all()

def save_session(session):
    _repo.save(session)

def summarize_session(session: Session) -> str:
    messages = session.history.messages
    if not messages:
        return "No messages to summarize."

    from di import container

    llm_service = container.resolve(LlmService)

    conversation = "\n".join(f"{m.role}: {m.content}" for m in session.history.messages)
    project_metadata = session.state.project_metadata or {}
    building_blocks = [bb.to_dict() for bb in session.state.building_blocks]

    prompt = f"""
    You are summarizing a development session in ASP.NET Core Domain-Driven Design (DDD) project built with OpenDDD.NET.
    The goal is to preserve meaningful context to continue development later, without needing the full history.

    Here is the conversation that took place:
    {conversation}

    Here is the current project metadata:
    {json.dumps(project_metadata, indent=2)}

    Here are the building blocks (aggregates, services, listeners, etc.):
    {json.dumps(building_blocks, indent=2)}

    Now, summarize this session:
    - What was the user trying to achieve?
    - What actions were taken?
    - What changes were made to the domain model?
    - What should the assistant remember to continue development?

    Summary:"""

    summary = llm_service.call_prompt(prompt).strip()
    session.apply_compaction(summary)
