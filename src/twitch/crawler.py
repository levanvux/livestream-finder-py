from pathlib import Path
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

state_file_name = "twitch_state.json"
state_file = Path(__file__).parent / state_file_name

try:
    raw_content = state_file.read_text(encoding="utf-8")

    states = json.loads(raw_content)

    if "access_token" in states:
        access_token = states["access_token"]
    else:
        print(f"In file {state_file_name}, key 'access_token' is not found")

except FileNotFoundError:
    print(f"State file not found: {state_file_name}")
except json.JSONDecodeError:
    print(f"Invalid JSON format in file: {state_file_name}")


try:
    response = requests.get(
        "https://api.twitch.tv/helix/streams?type=live&language=en&first=100",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Client-Id": os.getenv("TWITCH_CLIENT_ID"),
        },
    )

    data = response.json()
    # print(json.dumps(data, indent=4))

    streams = data.get("data", [])
    print("\n" + "=" * 60)
    print(f"🔥 SỐ LƯỢNG LIVESTREAM TÌM THẤY TRÊN TWITCH: {len(streams)}")
    print("=" * 60)

    for i, stream in enumerate(streams, start=1):

        print(f"\n#{i}")

        print(f"👤 Tên streamer: {stream['user_name']}")
        print(f"🎮 Thể loại: {stream['game_name']}")
        print(f"👀 Số người xem: {stream['viewer_count']:,}")
        print(f"🌎 Ngôn ngữ: {stream['language']}")
        print(f"\n📝 Tiêu đề: {stream["title"]}")
        print(f"\n🔗 Link: https://twitch.tv/{stream['user_login']}")

        print("\n" + "-" * 60)
except:
    print("Cannot fetch streams")
