from dataclasses import dataclass
from typing import Optional

from domain.model.intents.database_provider import DatabaseProvider
from domain.model.intents.persistence_provider import PersistenceProvider


@dataclass
class RepositoryImplementation:
    persistence: PersistenceProvider
    database: Optional[DatabaseProvider] = None
