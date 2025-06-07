from dataclasses import dataclass
from typing import List, Optional

from domain.model.intents.parameter import Parameter


@dataclass
class Method:
    name: str
    parameters: Optional[List[Parameter]] = None
    return_type: Optional[str] = None
    is_async: Optional[bool] = True
