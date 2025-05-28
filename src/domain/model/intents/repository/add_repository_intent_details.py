from dataclasses import dataclass
from typing import List

from domain.model.intents.method import Method
from domain.model.intents.repository.repository_implementation import \
    RepositoryImplementation


@dataclass
class AddRepositoryIntentDetails:
    custom_methods: List[Method]
    implementations: List[RepositoryImplementation]
