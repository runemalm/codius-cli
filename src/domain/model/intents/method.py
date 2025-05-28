from dataclasses import dataclass
from typing import List, Optional
from domain.model.intents.property import Property


@dataclass
class Method:
    name: str
    parameters: List[Property] = None
    return_type: Optional[str] = None
    is_async: bool = True
