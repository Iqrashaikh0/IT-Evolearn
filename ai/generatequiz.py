import os
import json
import requests
from dotenv import load_dotenv

# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


# =========================================================
# GENERATE QUIZ
# =========================================================

def generate_quiz(chapter):

    prompt = f"""
Create exactly 10 multiple-choice questions from this chapter.

Chapter:
{chapter}

Rules:

- Generate exactly 10 questions.
- Each question must have exactly 4 options.
- Only one option must be correct.
- Questions must be clear and exam-oriented.
- Use simple English.
- Questions should test understanding, not only memorization.
- Do not add explanations.
- Return ONLY valid JSON.
- Do not use Markdown.
- The "answer" value MUST exactly match one of the four options.
- Do not write A, B, C or D as the answer.
- Write the complete correct option as the answer.
- Do not add any text before or after the JSON.

Return exactly this format:

[
  {{
    "question": "Question text",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Option A"
  }}
]
"""

    # =====================================================
    # API HEADERS
    # =====================================================

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }


    # =====================================================
    # API DATA
    # =====================================================

    data = {

        "model": "openrouter/free",

        "messages": [

            {
                "role": "user",
                "content": prompt
            }

        ]

    }


    # =====================================================
    # SEND REQUEST
    # =====================================================

    try:

        response = requests.post(

            "https://openrouter.ai/api/v1/chat/completions",

            headers=headers,

            json=data,

            timeout=60

        )


        # =================================================
        # CHECK RESPONSE
        # =================================================

        if response.status_code != 200:

            return []


        result = response.json()


        if "choices" not in result:

            return []


        # =================================================
        # GET AI RESPONSE
        # =================================================

        text = result["choices"][0]["message"]["content"]


        if not text:

            return []


        # =================================================
        # CLEAN JSON
        # =================================================

        text = text.strip()

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        text = text.strip()


        # =================================================
        # CONVERT JSON
        # =================================================

        questions = json.loads(
            text
        )


        if not isinstance(
            questions,
            list
        ):

            return []


        # =================================================
        # VALIDATE QUESTIONS
        # =================================================

        valid_questions = []


        for q in questions:

            if not isinstance(
                q,
                dict
            ):

                continue


            if "question" not in q:

                continue


            if "options" not in q:

                continue


            if "answer" not in q:

                continue


            options = q["options"]

            answer = q["answer"]


            # ---------------------------------------------
            # Options validation
            # ---------------------------------------------

            if not isinstance(
                options,
                list
            ):

                continue


            if len(options) != 4:

                continue


            # ---------------------------------------------
            # Clean options
            # ---------------------------------------------

            cleaned_options = [

                str(option).strip()

                for option in options

            ]


            # ---------------------------------------------
            # Clean answer
            # ---------------------------------------------

            cleaned_answer = str(
                answer
            ).strip()


            # ---------------------------------------------
            # Correct answer MUST be one option
            # ---------------------------------------------

            if cleaned_answer not in cleaned_options:

                continue


            # ---------------------------------------------
            # Save valid question
            # ---------------------------------------------

            valid_questions.append({

                "question": str(
                    q["question"]
                ).strip(),

                "options": cleaned_options,

                "answer": cleaned_answer

            })


        # =================================================
        # RETURN MAXIMUM 10 QUESTIONS
        # =================================================

        return valid_questions[:10]


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception:

        return []

