import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_recommendation(chapter, score):

    prompt = f"""
A student has completed the quiz.

Chapter:
{chapter}

Score:
{score}/10

Generate a personalized study recommendation.

Requirements:

- Congratulate the student based on their performance.
- Explain what the score means.
- Mention strengths.
- Mention areas that need improvement.
- Suggest whether the student should revise the notes.
- Suggest using the Ask AI feature for doubts.
- Suggest whether the student should retake the quiz.
- Suggest if the student is ready to move to the next chapter.
- Use simple English.
- Keep the recommendation between 150 and 250 words.
- Do not mention AI or ChatGPT.
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek/deepseek-r1-0528:free",   # Use the model available in your OpenRouter account
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.5,
        "max_tokens": 600
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        return f"Error: {response.text}"

    result = response.json()

    if "choices" not in result:
        return f"OpenRouter Error:\n{result}"

    return result["choices"][0]["message"]["content"]