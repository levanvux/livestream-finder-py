import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class Gemini:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.model = model
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    def generate(self, prompt: str):
        return self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
