from dataclasses import dataclass
from domain.model.intents.intent_base import IntentBase
from domain.model.intents.intent import IntentType
from domain.model.intents.repository.add_repository_intent_details import AddRepositoryIntentDetails


@dataclass
class AddRepositoryIntent(IntentBase):
    intent: IntentType = IntentType.ADD_REPOSITORY
    target: str = ""
    details: AddRepositoryIntentDetails = None

    def to_example_json(self) -> str:
        return """{
  "intent": "add_repository",
  "target": "Order",
  "details": {
    "custom_methods": [
      {
        "name": "GetByExternalReferenceAsync",
        "parameters": [
          { "name": "externalReference", "type": "str" }
        ],
        "return_type": "Order",
        "is_async": true
      },
      {
        "name": "FindOpenOrdersAsync",
        "parameters": [],
        "return_type": "List<Order>",
        "is_async": true
      },
      {
        "name": "CountOrdersByCustomerAsync",
        "parameters": [
          { "name": "customerId", "type": "Guid" }
        ],
        "return_type": "int",
        "is_async": true
      }
    ],
    "implementations": [
      { "persistence": "EFCore" },
      { "persistence": "OpenDDD", "database": "Postgres" }
    ]
  }
}"""
