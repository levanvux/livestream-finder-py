from src.ai.gemini import Gemini
import time
import json

exhausted_models = set()


def classify_event(title: str, description: str):
    # Prompt cho Gemini:
    # Phân tích livestream và trả về JSON: industry, language, buyer_persona, score, reason, suggested_comment
    #
    # score (0-100): Mức độ đáng tham gia để tìm khách hàng tiềm năng.
    prompt = f"""
Analyze this livestream.

Title:
{title}

Description:
{description}

Objective:

Identify whether this livestream is worth monitoring or joining for business networking, lead generation, and relationship building within AI, Automation, SaaS, Startup, Recruiting Technology, Productivity, and related business sectors.

Priority is to discover livestreams attended by potential decision makers such as:

* Founder
* CEO
* CTO
* Startup Owner
* Business Owner
* Recruiter
* HR Manager
* Hiring Manager
* Operations Leader
* Agency Owner
* AI Consultant
* Automation Consultant
* Technology Decision Maker

Tasks:

1. Identify industry
2. Identify primary language
3. Identify likely buyer persona
4. Estimate livestream popularity level
5. Score opportunity from 0-100
6. Explain the score
7. Generate a human-like natural viewer comment

Important scoring rules:

Language requirement:

* English livestreams may receive any score from 0-100.
* Non-English livestreams should rarely exceed 50.
* Non-English livestreams must never exceed 69 unless there is exceptionally strong evidence of high-value international business participation.

Industry priority:

Highest priority:

* Artificial Intelligence
* AI Agents
* Automation
* No-Code / Low-Code
* SaaS
* Startup
* Recruiting Technology
* HR Technology
* Productivity Technology
* Business Operations
* Entrepreneurship

Medium priority:

* Software Development
* Data Science
* Cloud
* DevOps
* Cybersecurity

Low priority:

* Gaming
* Entertainment
* Music
* Sports
* General Lifestyle
* Politics
* Religion

Popularity estimation:

Estimate:

* Small
* Medium
* Large
* Major Industry Event

Use clues from title, host, guests, brands, event names, and context.

Scoring guide:

0-20
Irrelevant audience

21-40
Limited business value

41-69
Some relevance but not worth prioritizing

70-84
Good opportunity worth monitoring

85-94
High-priority livestream with strong business potential

95-100
Exceptional opportunity likely to attract high-value decision makers

Comment requirements:

The suggested_comment should:

* Sound like a real viewer
* Be natural and conversational
* Show curiosity or experience
* React to a likely discussion topic
* Avoid generic compliments
* Avoid marketing language
* Avoid sounding generated
* Maximum 20 words
* Exactly one sentence

Return ONLY valid JSON.

Example:

{{
"industry": "AI Automation",
"language": "English",
"buyer_persona": "Founder, CTO, AI Consultant",
"popularity": "Large",
"score": 88,
"reason": "English livestream focused on AI automation with strong likelihood of attracting founders and technical decision makers.",
"suggested_comment": "How are teams handling agent reliability once workflows become production critical?"
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
                        "suggested_comment": None,
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
        "suggested_comment": None,
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
