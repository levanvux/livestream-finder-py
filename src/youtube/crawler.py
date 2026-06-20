from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))


def search_live(keyword, limit):

    response = (
        youtube.search()
        .list(
            part="snippet", q=keyword, type="video", eventType="live", maxResults=limit
        )
        .execute()
    )

    return response


def crawl_youtube_live(keywords, limit):

    events = []
    seen_video_ids = set()

    for keyword in keywords:

        response = search_live(keyword, limit)

        for item in response["items"]:
            video_id = item["id"]["videoId"]

            if video_id in seen_video_ids:
                continue

            seen_video_ids.add(video_id)

            events.append(
                {
                    "title": item["snippet"]["title"],
                    "platform": "YouTube",
                    "url": (f"https://youtube.com/watch?v={video_id}"),
                    "description": item["snippet"]["description"],
                    "keyword": keyword,
                    "start_time": item["snippet"]["publishedAt"],
                }
            )

    return events
