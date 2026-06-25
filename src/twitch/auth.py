from pathlib import Path
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


response = requests.post(
    "https://id.twitch.tv/oauth2/token",
    params={
        "client_id": os.getenv("TWITCH_CLIENT_ID"),
        "client_secret": os.getenv("TWITCH_CLIENT_SECRET"),
        "grant_type": "client_credentials",
    },
)

token_data = response.json()

state_file = Path(__file__).with_name("twitch_state.json")
with state_file.open("w", encoding="utf-8") as f:
    json.dump(token_data, f, indent=4)

print(f"Twitch access token saved to: {state_file.name}")
