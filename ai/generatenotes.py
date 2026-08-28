import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


# =====================================================
# CHAPTER CONTENT
# =====================================================

CHAPTER_CONTENT = {

    "computerbasics": """
Computer Basics

Topics:
1. Introduction to Computers
2. Characteristics of Computers
3. Types of Computers
4. Components of a Computer
5. Hardware
6. Software
7. Input Devices
8. Output Devices
9. CPU
10. Memory
11. Storage Devices
12. Operating System
13. Applications of Computers
14. Advantages and Limitations of Computers
""",


    "internetsafety": """
Internet Safety

Topics:
1. Introduction to Internet Safety
2. Online Privacy
3. Personal Information
4. Strong Passwords
5. Cyber Threats
6. Phishing
7. Malware
8. Safe Browsing
9. Secure Websites
10. Social Media Safety
11. Cyberbullying
12. Online Scams
13. Digital Footprint
14. Responsible Internet Usage
"""
}


# =====================================================
# GENERATE NOTES
# =====================================================

def generate_notes(chapter):

    # Get actual chapter content
    chapter_content = CHAPTER_CONTENT.get(
        chapter.lower(),
        chapter
    )


    # =================================================
    # PROMPT
    # =================================================

    prompt = f"""
You are an educational content generator.

Create detailed study notes for the following chapter.

CHAPTER:
{chapter_content}


REQUIREMENTS:

1. Write detailed notes suitable for secondary school students.

2. Use simple and easy-to-understand English.

3. Explain every topic properly.

4. Do not skip any important topic.

5. Include:
   - Definitions
   - Detailed explanations
   - Types
   - Components
   - Functions
   - Examples
   - Advantages where applicable
   - Disadvantages where applicable
   - Important points

6. Use proper headings and subheadings.

7. Use bullet points wherever appropriate.

8. Give real-life examples where possible.

9. Make the notes useful for exam preparation.

10. Do not make the notes extremely short.

11. Do not mention AI anywhere in the notes.

12. Do not add unnecessary introduction or comments.

13. Do not write questions unless they are necessary for explaining a concept.

14. Keep the language student-friendly.


USE THIS FORMAT:

# Chapter Title

## 1. Topic Name

### Definition

Explain the topic clearly.

### Detailed Explanation

Explain the concept in detail.

### Types / Components / Functions

- Point 1
- Point 2
- Point 3

### Example

Give a simple example.

### Important Points

- Important point 1
- Important point 2
- Important point 3


Continue the same structure for all topics.


## Key Points for Revision

- Important point
- Important point
- Important point


## Chapter Summary

Give a clear and complete summary of the chapter.


IMPORTANT:
- Cover all listed topics.
- Maintain correct technical information.
- Use simple English.
- Make the content detailed enough for studying.
- Do not mention AI.
"""


    # =================================================
    # CHECK API KEY
    # =================================================

    if not API_KEY:

        return "Error: OPENROUTER_API_KEY is not configured."


    # =================================================
    # API REQUEST
    # =================================================

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

        ],

        "temperature": 0.7
    }


    try:

        response = requests.post(

            "https://openrouter.ai/api/v1/chat/completions",

            headers=headers,

            json=data,

            timeout=60
        )


        result = response.json()


        # =============================================
        # API ERROR
        # =============================================

        if response.status_code != 200:

            return (
                "OpenRouter Error:\n"
                + str(result)
            )


        if "choices" not in result:

            return (
                "OpenRouter Error:\n"
                + str(result)
            )


        # =============================================
        # RETURN NOTES
        # =============================================

        return result["choices"][0]["message"]["content"]


    except requests.exceptions.Timeout:

        return "Error: OpenRouter request timed out. Please try again."


    except requests.exceptions.RequestException as e:

        return f"Connection Error: {str(e)}"


    except Exception as e:

        return f"Unexpected Error: {str(e)}"