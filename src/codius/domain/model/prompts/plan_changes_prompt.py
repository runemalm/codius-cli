from dataclasses import dataclass
from typing import Dict
from codius.domain.model.plan.steps.create_file_step import CreateFileStep
from codius.domain.model.plan.steps.modify_file_step import ModifyFileStep


@dataclass(frozen=True)
class PlanChangesPrompt:
    intents: list
    sources: Dict[str, str]
    project_metadata: dict

    def as_prompt(self) -> str:
        example_steps = [
            CreateFileStep(
                path="Domain/Model/Order/Order.cs",
                description="Create Order aggregate",
                template="domain/model/aggregate/aggregate_root",
                context={
                    "aggregate_name": "Order",
                    "namespace": "MyApp.Domain.Model.Order",
                    "properties": [],
                    "events": [],
                    "commands": []
                }
            ),
            ModifyFileStep(
                path="Domain/Model/Order/Order.cs",
                description="Add SummarizeLines method to Order",
                modification="add_method",
                context={
                    "aggregate_name": "Order",
                    "method": {
                        "name": "SummarizeLines",
                        "parameters": [],
                        "returns": "OrderSummaryDto",
                        "body": "return new OrderSummaryDto(Lines.Count, Lines.Sum(l => l.Price));"
                    },
                    "placement": {
                        "type": "after_method",
                        "reference": "AddLine"
                    }
                }
            )
        ]

        example_blocks = "\n".join(
            f"### {step.description}\n```json\n{step.to_example_json()}\n```"
            for step in example_steps
        )

        supported_templates = [
            "domain/model/aggregate/aggregate_root",
            "domain/model/value_object/value_object",
            # Add more here as needed
        ]

        template_section = "\n".join(f"- {t}" for t in supported_templates)

        sources_section = "\n\n".join(
            f"### File: {path}\n```csharp\n{content.strip()}\n```"
            for path, content in self.sources.items()
        )

        project_context = f"""
Domain path: {self.project_metadata.get('domain_path')}
Application path: {self.project_metadata.get('application_path')}
Infrastructure path: {self.project_metadata.get('infrastructure_path')}
Root namespace: {self.project_metadata.get('root_namespace')}
Persistence provider: {self.project_metadata.get('persistence_provider')}
Database provider: {self.project_metadata.get('database_provider')}
"""

        import json
        intents_json = json.dumps(self.intents, indent=2)

        return f"""
You are a Domain-Driven Design (DDD) planning assistant for OpenDDD.NET.

Your task is to plan the necessary code changes for the following modeling intents based on the current project metadata and source files.

For each intent:

- Determine if a new file must be created or an existing file modified.
- Describe each code change as a **plan step** using a JSON object with:
  - `"type"`: `"create_file"` or `"modify_file"`.
  - `"path"`: relative path where the file is created or modified.
  - `"description"`: a short explanation of the change.
  - For `"create_file"`:
    - `"template"`: the name of the template used. Must match one of the supported templates listed below.
    - `"context"`: all required data for the template.
  - For `"modify_file"`:
    - `"modification"`: the kind of modification (`add_method`, `add_property`, etc.).
    - `"context"`: details about what to add or change.

✅ All C# class, method, and property names must use PascalCase.  
✅ Only return a **JSON list of plan steps** — no markdown, no explanations, no comments.

---

## Supported Templates:

{template_section}

---

## Project Metadata:
{project_context}

---

## Modeling Intents:

```json
{intents_json}
```

---

## Source Files:

{sources_section}

---

## Example Plan Steps:

{example_blocks}
"""
