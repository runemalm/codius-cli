from dataclasses import dataclass
from domain.model.intents.intent_base import IntentBase
from domain.model.intents.intent_type import IntentType
from infrastructure.services.code_scanner.model.building_block_type import \
    BuildingBlockType


@dataclass
class RemoveValueObjectPropertyIntent(IntentBase):
    intent: IntentType = IntentType.REMOVE_VALUE_OBJECT_PROPERTY
    building_block_type: BuildingBlockType = BuildingBlockType.VALUE_OBJECT
    target: str = ""
    property_name: str = ""

    @classmethod
    def to_example_json(cls) -> str:
        return """{
  "intent": "remove_value_object_property",
  "target": "Address",
  "property_name": "ZipCode"
}"""
