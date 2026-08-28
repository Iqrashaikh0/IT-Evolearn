import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def ask_ai_response(chapter, question):

    prompt = f"""
You are a helpful AI tutor.
Chapter:
{chapter}
Student Question:
{question}

Answer rules:
- Explain in simple English.
- Give examples.
- Be clear and educational.
- Do not mention AI.
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }


    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()
    if "choices" not in result:
        return "API Error: " + str(result)
    return result["choices"][0]["message"]["content"]