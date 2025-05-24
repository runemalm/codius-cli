from dataclasses import dataclass


@dataclass(frozen=True)
class GenerateCodePrompt:
    plan: dict
    domain_summary: str

    def as_prompt(self) -> str:
        return f"""
You are a senior .NET developer using the OpenDDD.NET framework.

Here is the current domain model:
{self.domain_summary or '[Empty domain]'}

Here is the tactical plan to implement:
{self.plan}

Generate the code files needed to apply this plan. Use clean .NET 8 syntax and follow OpenDDD conventions.

Return JSON like this:
{{
  "files": [
    {{
      "path": "Domain/Order/ProductBundle.cs",
      "content": "<full file content>"
    }},
    ...
  ]
}}
"""
