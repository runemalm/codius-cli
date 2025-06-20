from dataclasses import dataclass
from typing import List, Optional

from domain.model.intents.location import Location
from domain.model.intents.method_implementation import MethodImplementation
from domain.model.intents.parameter import Parameter


@dataclass
class Method:
    name: str
    parameters: Optional[List[Parameter]] = None
    return_type: Optional[str] = None
    is_async: Optional[bool] = True
    location: Optional[Location] = None
    implementation: Optional[MethodImplementation] = None
