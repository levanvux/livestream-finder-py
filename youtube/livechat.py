from urllib.parse import urlparse, parse_qs
from auth import get_youtube_client


def get_live_chat_id(video_url: str):
    youtube = get_youtube_client()
    video_id = parse_qs(urlparse(video_url).query)["v"][0]

    response = (
        youtube.videos()
        .list(
            part="liveStreamingDetails",
            id=video_id,
        )
        .execute()
    )

    items = response.get("items", [])

    if not items:
        return None

    details = items[0].get("liveStreamingDetails", {})
    print(response)

    return details.get("activeLiveChatId")


def send_message(chat_id: str, text: str):
    youtube = get_youtube_client()

    response = (
        youtube.liveChatMessages()
        .insert(
            part="snippet",
            body={
                "snippet": {
                    "liveChatId": chat_id,
                    "type": "textMessageEvent",
                    "textMessageDetails": {
                        "messageText": text,
                    },
                }
            },
        )
        .execute()
    )

    return response


print(
    send_message(
        get_live_chat_id("https://www.youtube.com/watch?v=8vaOW_2EpLc"),
        "hi",
    )
)
