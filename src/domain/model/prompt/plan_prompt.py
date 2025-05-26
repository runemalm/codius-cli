from dataclasses import dataclass
from typing import List

from infrastructure.service.code_scanner.model.building_block import BuildingBlock


@dataclass(frozen=True)
class PlanPrompt:
    intent: dict
    building_blocks: List[BuildingBlock]

    def as_prompt(self) -> str:
        intent_type = self.intent.get("intent", "unknown")
        target = self.intent.get("target", "")
        layer = self.intent.get("layer", "")
        details = self.intent.get("details", {})

        description = details.get("description", "")
        properties = details.get("properties", [])
        events = details.get("events", [])
        commands = details.get("commands", [])

        blocks_summary = "\n".join(
            f"- {bb.type.value}: {bb.name} ({bb.namespace})"
            for bb in self.building_blocks
        ) or "[No existing building blocks]"

        return f"""
You are a modeling assistant for a .NET 8 project using Domain-Driven Design (DDD) with the OpenDDD.NET framework.

Below is a list of existing building blocks in the codebase:
{blocks_summary}

The user intends to perform the following modeling action:

Intent: {intent_type}
Target: {target}
Layer: {layer}
Description: {description}

Properties:
{chr(10).join(f"- {p['name']}: {p['type']}" for p in properties) or 'None'}

Events:
{', '.join(events) if events else 'None'}

Commands:
{', '.join(commands) if commands else 'None'}

Based on this, generate a list of proposed **file changes** needed to implement this modeling intent.

Respond only with a bulleted list of relative file paths. Example:

- Domain/Profile/Profile.cs
- Domain/Events/ProfileCreated.cs
- Application/Profile/CreateProfileAction.cs

Do not include explanations. Do not generate file contents. Just return the list of files.
"""