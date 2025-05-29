from dataclasses import dataclass
from abc import ABC
from domain.model.intents.intent_type import IntentType


@dataclass
class IntentBase(ABC):
    intent: IntentType

    def to_example_json(self) -> str:
        raise NotImplementedError("Subclasses must implement this method.")
