from dataclasses import dataclass
from domain.model.intents.intent_base import IntentBase
from domain.model.intents.intent_type import IntentType


@dataclass
class DeleteAggregateIntent(IntentBase):
    intent: IntentType = IntentType.DELETE_AGGREGATE
    target: str = ""

    def to_example_json(self) -> str:
        return """{
  "intent": "delete_aggregate",
  "target": "Person"
}"""
