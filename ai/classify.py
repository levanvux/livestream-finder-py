from gemini_client import client, DEFAULT_MODEL
import json


def classify_event(title: str, description: str):
    # Prompt cho Gemini:
    # Phân tích livestream và trả về JSON: industry, language, buyer_persona, score, reason
    #
    # score (0-100): Mức độ đáng tham gia để tìm khách hàng tiềm năng.
    prompt = f"""
Analyze this livestream.

Title:
{title}

Description:
{description}

Your task:

1. Identify industry
2. Identify primary language
3. Identify buyer persona
4. Score business opportunity from 0-100
5. Explain score

Target buyers include:
- Founder
- CEO
- CTO
- Recruiter
- HR Manager
- Startup Owner
- Business Decision Maker

Scoring guide:

0-20:
Irrelevant audience

21-50:
Weak opportunity

51-80:
Good opportunity

81-100:
Excellent opportunity

Return ONLY valid JSON.

Example:

{{
    "industry": "Recruitment",
    "language": "English",
    "buyer_persona": "Recruiter, HR Manager",
    "score": 92,
    "reason": "Audience contains hiring decision makers."
}}
"""

    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=prompt,
    )

    try:
        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "", 1)

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        return json.loads(text)

    except Exception:

        return {
            "industry": None,
            "language": None,
            "buyer_persona": None,
            "score": 0,
            "reason": response.text,
        }
