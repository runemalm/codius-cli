from dataclasses import dataclass
from typing import List

from domain.model.intents.method import Method
from domain.model.intents.property import Property


@dataclass
class AddAggregateIntentDetails:
    properties: List[Property]
    methods: List[Method]
