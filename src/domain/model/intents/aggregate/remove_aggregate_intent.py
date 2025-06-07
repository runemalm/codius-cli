from dataclasses import dataclass
from domain.model.intents.intent_base import IntentBase
from domain.model.intents.intent_type import IntentType
from infrastructure.services.code_scanner.model.building_block_type import \
    BuildingBlockType


@dataclass
class RemoveAggregateIntent(IntentBase):
    intent: IntentType = IntentType.REMOVE_AGGREGATE
    building_block_type: BuildingBlockType = BuildingBlockType.AGGREGATE_ROOT
    target: str = ""

    @classmethod
    def to_example_json(cls) -> str:
        return """{
  "intent": "remove_aggregate",
  "target": "Person"
}"""
