import re

import openai
import json

from domain.service.config_service import get_config_value


def call_llm(prompt: str, model: str = "gpt-4o") -> dict:
    try:
        # Get API key from config
        api_key = get_config_value("openai_api_key")
        if not api_key or not api_key.startswith("sk-"):
            return {
                "intent": None,
                "error": "Missing or invalid OpenAI API key in .openddd/config.yaml"
            }

        # Create OpenAI client
        client = openai.OpenAI(api_key=api_key)

        # Call the chat model
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )

        content = response.choices[0].message.content

        # Extract JSON if wrapped in triple backticks (```json\n...\n```)
        match = re.search(r"```(?:json)?\s*(.*?)```", content, re.DOTALL)
        json_text = match.group(1).strip() if match else content.strip()

        return json.loads(json_text)

    except json.JSONDecodeError:
        return {"intent": None, "raw": content}

    except Exception as e:
        return {"intent": None, "error": str(e)}
