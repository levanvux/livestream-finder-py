from ai.gemini import Gemini
import time
import json

exhausted_models = set()


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

    gemini_models = [
        "gemini-2.5-flash",
        "gemini-3.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-3.1-flash-lite",
    ]

    for model in gemini_models:

        if model in exhausted_models:
            continue

        for retry in range(2):

            try:
                print(f"🤖 Gemini: {model} " f"(attempt {retry + 1}/2)")

                gemini = Gemini(model)
                response = gemini.generate(prompt)

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
            except Exception as e:

                error = str(e)

                if "RESOURCE_EXHAUSTED" in error:

                    print(f"⚠️ Quota exhausted on {model}")

                    time.sleep(61)

                    if retry == 1:
                        exhausted_models.add(model)

                    continue

                print(f"❌ Error on {model}: {error}")

                break

    return {
        "industry": None,
        "language": None,
        "buyer_persona": None,
        "score": 0,
        "reason": "Gemini models exhausted or failed. Try again tomorrow.",
    }


# === FOR TESTING PURPOSE ===

# print(
#     classify_event(
#         " 24/7 Live Business Website & App Development Promo | Website Starting ₹8,000 ",
#         "Welcome to our 24/7 live promo stream.We provide professional Website Development, Mobile App Development, CRM Software, SaaS Solutions and Custom Business Software for small businesses, startups, consultants, doctors, coaching classes, manufacturers and service providers.✅ Business Website Development  ✅ Mobile App Development  ✅ CRM / Custom Software  ✅ E-commerce Website  ✅ Hosting, Domain & SSL Setup  ✅ WhatsApp Inquiry Website  ",
#     )
# )


# print(
#     classify_event(
#         " How to walk and dance as a kid ",
#         "I made this video for fun. Watch if u are a kid :) ",
#     )
# )
