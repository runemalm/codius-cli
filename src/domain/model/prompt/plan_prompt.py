from dataclasses import dataclass


@dataclass(frozen=True)
class PlanPrompt:
    intent: dict

    def as_prompt(self) -> str:
        intent_type = self.intent.get("intent", "unknown")
        target = self.intent.get("target", "")
        layer = self.intent.get("layer", "")
        details = self.intent.get("details", {})

        description = details.get("description", "")
        properties = details.get("properties", [])
        events = details.get("events", [])
        commands = details.get("commands", [])

        return f"""
You are a modeling assistant for a DDD project using the OpenDDD.NET framework.

The user intends to perform the following modeling action:

Intent: {intent_type}
Target: {target}
Layer: {layer}
Description: {description}

Properties:
{chr(10).join(f"- {p['name']}: {p['type']}" for p in properties)}

Events:
{', '.join(events) if events else 'None'}

Commands:
{', '.join(commands) if commands else 'None'}

Based on this, list the proposed file changes required to implement this modeling intent.

Respond only with a bulleted list of relative file paths, e.g.:

- Domain/Model/Order.cs
- Domain/Events/OrderPlaced.cs
- Application/PlaceOrder/PlaceOrderAction.cs

Do not include explanations. Do not generate content. Just list the necessary new or modified files.
"""
