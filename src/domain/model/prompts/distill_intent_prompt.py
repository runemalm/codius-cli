from dataclasses import dataclass
from domain.model.intents.aggregate.add_aggregate_intent import AddAggregateIntent
from domain.model.intents.aggregate.delete_aggregate_intent import DeleteAggregateIntent
from domain.model.intents.database_provider import DatabaseProvider
from domain.model.intents.persistence_provider import PersistenceProvider
from domain.model.intents.repository.add_repository_intent import AddRepositoryIntent
from domain.model.intents.intent_type import IntentType


@dataclass(frozen=True)
class DistillIntentPrompt:
    summary: str
    user_input: str

    def as_prompt(self) -> str:
        example_blocks = "\n\n### add_aggregate\n```json\n" + \
                         AddAggregateIntent().to_example_json() + \
                         "\n```\n\n### add_repository\n```json\n" + \
                         AddRepositoryIntent().to_example_json() + \
                         "\n```\n\n### delete_aggregate\n```json\n" + \
                         DeleteAggregateIntent().to_example_json() + \
                         "\n```"

        supported_intents = [
            f"- {intent.value}"
            for intent in IntentType
            if intent != IntentType.UNSURE
        ]
        supported_intents_text = "\n".join(supported_intents)

        persistence_providers = [f"- {p.value}" for p in PersistenceProvider]
        database_providers = [f"- {d.value}" for d in DatabaseProvider]

        persistence_text = "\n".join(persistence_providers)
        database_text = "\n".join(database_providers)

        context_section = f"""
### Context

Previous modeling session summary:

{self.summary.strip()}

""" if self.summary else ""

        return f"""
You are a modeling assistant for a Domain-Driven Design (DDD) codebase built with OpenDDD.NET.

{context_section}
The user has written the following instruction:

"{self.user_input}"

Your task is to extract the modeling **intent** from this instruction and return it as a **valid JSON object**.

You may only choose from the following supported intents:

{supported_intents_text}

For `"add_repository"` intents, the supported values are:

**Persistence Providers**:
{persistence_text}

**Database Providers**:
{database_text}

### Instructions

- Only include properties or methods if the user explicitly describes them.
- For repository `custom_methods`, return full method objects with:
    - `"name"` (required)
    - `"parameters"` (optional list of objects with `"name"` and `"type"`)
    - `"return_type"` (optional string, if the user hints at the expected result)
    - `"is_async"` (optional, defaults to `true` if unspecified)
- If the user simply asks to create a building block without specifying any structure, generate a minimal scaffold (e.g. an empty class or interface).
- Do not infer or add anything the user hasn’t clearly stated.
- Avoid comments or docstrings unless necessary to clarify complex logic in rare cases.
- Return **valid JSON only** — no prose, no comments, no extra text.

### Examples:

{example_blocks}

If the user's intent is unclear or unsupported, respond only with:

```json
{{ "intent": "unsure" }}
```
"""
