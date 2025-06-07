from dataclasses import dataclass
from domain.model.intents.intent_base import IntentBase
from domain.model.intents.intent_type import IntentType
from domain.model.intents.method import Method
from infrastructure.services.code_scanner.model.building_block_type import \
    BuildingBlockType


@dataclass
class AddAggregateMethodIntent(IntentBase):
    intent: IntentType = IntentType.ADD_AGGREGATE_METHOD
    building_block_type: BuildingBlockType = BuildingBlockType.AGGREGATE_ROOT
    target: str = ""
    method: Method = None

    @classmethod
    def to_example_json(cls) -> str:
        return """{
  "intent": "add_aggregate_method",
  "target": "Person",
  "method": {
    "name": "Deactivate",
    "parameters": [],
    "return_type": "void",
    "is_async": false
  }
}"""
