import json
from pathlib import Path
from domain.model.session import Session
from domain.model.state import State
from domain.model.history import History, Message
from infrastructure.repository.base_repository import BaseRepository

SESSIONS_DIR = Path(".openddd/sessions")
ACTIVE_FILE = SESSIONS_DIR / "active"


class SessionRepository(BaseRepository[Session]):

    def get(self, id: str) -> Session:
        session_path = SESSIONS_DIR / id
        state_path = session_path / "state.json"
        history_path = session_path / "history.json"

        # Load state
        if state_path.exists():
            state_data = json.loads(state_path.read_text())
            state = State(**state_data)
        else:
            state = State()

        # Load history
        if history_path.exists():
            history_data = json.loads(history_path.read_text())
            messages = [Message(**m) for m in history_data]
            history = History(messages)
        else:
            history = History()

        return Session(id=id, state=state, history=history)

    def get_all(self) -> list[Session]:
        if not SESSIONS_DIR.exists():
            return []
        return [
            self.get(p.name)
            for p in SESSIONS_DIR.iterdir()
            if p.is_dir() and p.name != "active"
        ]

    def save(self, session: Session) -> None:
        session_path = SESSIONS_DIR / session.id
        session_path.mkdir(parents=True, exist_ok=True)
        (session_path / "generated").mkdir(exist_ok=True)

        # Save state and history
        (session_path / "state.json").write_text(json.dumps(session.state.__dict__, indent=2))
        messages = [m.__dict__ for m in session.history.messages]
        (session_path / "history.json").write_text(json.dumps(messages, indent=2))

        # Update active session pointer
        ACTIVE_FILE.write_text(session.id)

    def delete(self, id: str) -> None:
        path = SESSIONS_DIR / id
        if path.exists():
            for file in path.glob("*"):
                file.unlink()
            path.rmdir()

    def get_active_session(self) -> Session:
        session_id = ACTIVE_FILE.read_text().strip()
        return self.get(session_id)
