from dataclasses import dataclass


@dataclass(frozen=True)
class DistillIntentPrompt:
    user_input: str

    def as_prompt(self) -> str:
        return f"""
You are a modeling assistant for a Domain-Driven Design (DDD) codebase built with OpenDDD.NET.

The user has written the following instruction:

"{self.user_input}"

Your task is to extract the modeling intent from this instruction and respond with a **structured JSON object**.

Use the following JSON format:

{{
  "intent": "add_aggregate",              // intent type
  "target": "Order",                      // the name of the concept (e.g. aggregate, action)
  "layer": "domain",                      // which layer it belongs to
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

Supported values for "intent" include:
- "add_aggregate"
- "generate_action"
- "create_domain_event"
- "generate_adapter"
- "update_value_object"
- "add_event_listener"
- "unsure"

If the user's request is unclear, respond only with:

{{ "intent": "unsure" }}

Return **valid JSON only** — no explanation, no comments.
"""
