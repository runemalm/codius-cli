from domain.model.session.session import Session
from domain.services.session_factory import create_session
from infrastructure.repository.session_repository import SessionRepository

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
