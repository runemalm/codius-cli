from dataclasses import dataclass, field
from domain.model.state import State
from domain.model.history import History

@dataclass
class Session:
    id: str
    state: State = field(default_factory=State)
    history: History = field(default_factory=History)

    def append_user_message(self, content: str):
        self.history.append("user", content)

    def append_assistant_message(self, content: str):
        self.history.append("assistant", content)
