import openai
import json


def call_llm(prompt: str, model: str = "gpt-4o") -> dict:
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )

        content = response.choices[0].message.content

        return json.loads(content)

    except json.JSONDecodeError:
        return {"intent": None, "raw": content}

    except Exception as e:
        return {"intent": None, "error": str(e)}
