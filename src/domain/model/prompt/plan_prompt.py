from dataclasses import dataclass


@dataclass(frozen=True)
class PlanPrompt:
    intent: dict
    domain_summary: str

    def as_prompt(self) -> str:
        return f"""
You are assisting with domain modeling in a .NET project using Domain-Driven Design.

Here is the current domain model:
{self.domain_summary or '[Empty domain]'}

User's intent:
{self.intent}

Based on this, propose a tactical plan using DDD patterns (e.g., CreateEntity, AddFieldToAggregate, CreateDomainEvent).
Respond only with JSON like this:

{{
  "plan": {{
    "tacticalChanges": [
      {{
        "type": "CreateEntity",
        "name": "ProductBundle",
        "fields": [
          {{ "name": "name", "type": "string" }},
          {{ "name": "products", "type": "List<Product>" }}
        ]
      }},
      {{
        "type": "AddFieldToAggregate",
        "aggregate": "Order",
        "field": {{ "name": "bundles", "type": "List<ProductBundle>" }}
      }}
    ]
  }}
}}
"""
