from dataclasses import dataclass, field

from domain.model.history import History
from domain.model.state import State


@dataclass
class Session:
    id: str
    state: State = field(default_factory=State)
    history: History = field(default_factory=History)

    def append_user_message(self, content: str):
        self.history.append("user", content)

    def append_assistant_message(self, content: str):
        self.history.append("assistant", content)

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
