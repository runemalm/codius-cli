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
  "target": "Order",                      // the name of the concept (e.g. aggregate, action, repository)
  "details": {{
      // Intent-specific fields go here.
      // For "add_aggregate": include description, properties, events, commands.
      // For "add_repository": include custom_methods, implementations (e.g. persistence/database providers).
      // For other intents: include any additional details the user provided.
  }}
}}

Note: You do **not** need to include a "layer" field — the assistant will infer the layer automatically based on the intent type.

Supported values for "intent" include:
- "add_aggregate"
- "add_repository"
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
