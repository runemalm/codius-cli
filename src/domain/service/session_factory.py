from datetime import datetime
from domain.model.session import Session


def create_session(name: str | None = None) -> Session:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    session_id = f"{name}_{timestamp}" if name else f"session_{timestamp}"
    return Session(id=session_id)
