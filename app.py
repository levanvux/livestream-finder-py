from crawler.meetup import crawl_meetup
from crawler.youtube import crawl_youtube_live
from ai.classify import classify_event
from database.livestream_repository import save_event


def process_event(event: dict):

    classify_result = classify_event(
        event["title"],
        event.get("description", ""),
    )

    event.update(classify_result)

    save_event(event)

    print("-" * 50)
    print(f"Title: {event['title']}")
    print(f"Platform: {event['platform']}")
    print(f"URL: {event['url']}")
    print(f"Keyword: {event.get('keyword')}")

    print(f"Industry: {event.get('industry')}")
    print(f"Language: {event.get('language')}")
    print(f"Buyer Persona: {event.get('buyer_persona')}")
    print(f"Score: {event.get('score')}")
    print(f"Reason: {event.get('reason')}")


def main():
    #  Định nghĩa danh sách các từ khóa cần tìm kiếm
    keywords = ["AI", "Recruiting", "Startup", "HR", "SaaS", "Fintech"]

    # meetup_events = crawl_meetup(keywords)

    # for event in meetup_events:

    #     print("-" * 50)

    #     print(f"Title: {event['title']}")

    #     print(f"Platform: {event['platform']}")

    #     print(f"URL: {event['url']}")

    #     print(f"Keyword: {event['keyword']}")

    # print(f"\n🎉 TỔNG SỐ EVENTS MEETUP TÌM ĐƯỢC: {len(meetup_events)}")

    youtube_live_events = crawl_youtube_live(keywords)

    for event in youtube_live_events:
        process_event(event)

    print(f"\n🎉 TỔNG SỐ EVENTS YOUTUBE LIVE TÌM ĐƯỢC: {len(youtube_live_events)}")


if __name__ == "__main__":
    main()
