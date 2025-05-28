from dataclasses import dataclass
from domain.model.intents.intent_base import IntentBase
from domain.model.intents.intent import IntentType
from domain.model.intents.aggregate.add_aggregate_intent_details import AddAggregateIntentDetails


@dataclass
class AddAggregateIntent(IntentBase):
    intent: IntentType = IntentType.ADD_AGGREGATE
    target: str = ""
    details: AddAggregateIntentDetails = None

    def to_example_json(self) -> str:
        return """{
  "intent": "add_aggregate",
  "target": "Person",
  "details": {
    "properties": [
      { "name": "Id", "type": "Guid" },
      { "name": "Name", "type": "string" }
    ],
    "methods": [
      {
        "name": "Rename",
        "parameters": [
          { "name": "newName", "type": "string" }
        ]
      }
    ]
  }
}"""
