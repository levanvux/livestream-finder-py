from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

load_dotenv()

youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))


def search_live(keyword):

    response = (
        youtube.search()
        .list(part="snippet", q=keyword, type="video", eventType="live", maxResults=25)
        .execute()
    )

    return response


def crawl_youtube_live(keywords):

    events = []

    for keyword in keywords:

        response = search_live(keyword)

        for item in response["items"]:

            video_id = item["id"]["videoId"]

            events.append(
                {
                    "title": item["snippet"]["title"],
                    "platform": "YouTube",
                    "url": (f"https://youtube.com/watch?v={video_id}"),
                    "description": item["snippet"]["description"],
                    "keyword": keyword,
                }
            )

    return events
