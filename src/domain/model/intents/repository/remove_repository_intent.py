from dataclasses import dataclass
from typing import Optional

from domain.model.intents.intent_base import IntentBase
from domain.model.intents.intent_type import IntentType
from domain.model.intents.persistence_provider import PersistenceProvider
from domain.model.intents.database_provider import DatabaseProvider
from infrastructure.services.code_scanner.model.building_block_type import \
    BuildingBlockType


@dataclass
class RemoveRepositoryIntent(IntentBase):
    intent: IntentType = IntentType.REMOVE_REPOSITORY
    building_block_type: BuildingBlockType = BuildingBlockType.REPOSITORY
    target: str = ""
    persistence_provider: Optional[PersistenceProvider] = None
    database_provider: Optional[DatabaseProvider] = None

    @classmethod
    def to_example_json(cls) -> str:
        return """{
  "intent": "remove_repository",
  "target": "Person",
  "persistence_provider": "OpenDdd",
  "database_provider": "Postgres"
}"""
