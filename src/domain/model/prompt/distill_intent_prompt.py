from dataclasses import dataclass


@dataclass(frozen=True)
class DistillIntentPrompt:
    user_input: str
    domain_summary: str

    def as_prompt(self) -> str:
        return f"""
You are a modeling assistant for a Domain-Driven Design (DDD) codebase that follows the conventions of the OpenDDD.NET framework.

Below is the current summary of the domain model:

{self.domain_summary}

The user has provided the following instruction:

"{self.user_input}"

Your task is to extract the user's modeling intent as a structured JSON object.

Respond only with JSON, using the following format:

{{
  "intent": "add_aggregate",              // or other supported intent
  "target": "Order",                      // name of the aggregate/action/etc.
  "layer": "domain",                      // domain, application, or infrastructure
  "details": {{
    "description": "Represents a customer order",
    "properties": [
      {{ "name": "id", "type": "Guid" }},
      {{ "name": "customerId", "type": "Guid" }},
      {{ "name": "lineItems", "type": "List<LineItem>" }}
    ],
    "events": ["OrderPlaced"],
    "commands": ["PlaceOrder"]
  }}
}}

Supported values for "intent" include (but are not limited to):
- "add_aggregate"
- "generate_action"
- "create_domain_event"
- "generate_adapter"
- "update_value_object"
- "add_event_listener"
- "unsure"

If the user's intent is unclear or not actionable, respond with:

{{ "intent": "unsure" }}

Do not include any commentary or explanation. Return valid JSON only.
"""
