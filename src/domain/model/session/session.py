from dataclasses import dataclass, field
from datetime import datetime, timedelta

from domain.model.session.history import History
from domain.model.session.state import State

SESSION_EXPIRY_HOURS = 6


@dataclass
class Session:
    id: str
    state: State = field(default_factory=State)
    history: History = field(default_factory=History)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def append_user_message(self, content: str):
        self.history.append("user", content)

    def append_assistant_message(self, content: str):
        self.history.append("assistant", content)

    def clear_state(self):
        """Resets both state and history."""
        self.state = State()

    def clear(self):
        """Resets both state and history."""
        self.state = State()
        self.history.clear()

    def clear_history(self):
        """Clears only history."""
        self.history.clear()

    def compact_history(self, summary: str | None = None):
        """Clears history but saves a compact summary into the state."""
        if summary:
            self.state.summary = summary
        elif self.state.intent:
            self.state.summary = f"Modeling session for intent: {self.state.intent}"
        else:
            self.state.summary = "Compact session without specific intent."
        self.history.clear()

    def should_be_replaced(self) -> bool:
        try:
            created = datetime.fromisoformat(self.created_at)
            is_old = datetime.utcnow() - created > timedelta(hours=SESSION_EXPIRY_HOURS)
        except Exception:
            is_old = False

        compacted = bool(self.state.summary)
        has_new_messages = len(self.history.messages) > 0

        return (compacted and not has_new_messages) or is_old
