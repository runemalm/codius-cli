from dataclasses import dataclass, field
import datetime

from domain.model.message import Message


@dataclass
class History:
    messages: list[Message] = field(default_factory=list)

    def append(self, role: str, content: str):
        self.messages.append(
            Message(role=role, content=content, timestamp=datetime.datetime.utcnow().isoformat())
        )

    def recent(self, n=4) -> list[Message]:
        return self.messages[-n:]
