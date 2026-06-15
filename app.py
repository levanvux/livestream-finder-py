from crawler.meetup import crawl_meetup
from crawler.youtube import crawl_youtube_live
from ai.classify import classify_event
from database.livestream_repository import save_event
from youtube.livechat import get_live_chat_id, send_message


def try_comment(event: dict):
    # Hiện tại chỉ có thể comment YouTube
    if event["platform"] != "YouTube":
        return

    # Chỉ comment vào livestream được AI đánh giá là chất lượng cao
    if event.get("score") < 80:
        return

    comment = event.get("suggested_comment")

    if not comment:
        return

    chat_id = get_live_chat_id(event["url"])

    if not chat_id:
        print("No active chat")
        return

    try:
        send_message(chat_id, comment)
        print("Comment sent:", comment)

    except Exception as e:
        print("Comment failed:", e)


def process_event(event: dict):

    classify_result = classify_event(
        event["title"],
        event.get("description", ""),
    )

    event.update(classify_result)

    save_event(event)

    try_comment(event)

    print("-" * 50)
    print(f"Title: {event['title']}")
    print(f"Platform: {event['platform']}")
    print(f"URL: {event['url']}")
    print(f"Keyword: {event.get('keyword')}")
    print(f"Start time: {event.get('start_time')}")

    print(f"Industry: {event.get('industry')}")
    print(f"Language: {event.get('language')}")
    print(f"Buyer Persona: {event.get('buyer_persona')}")
    print(f"Score: {event.get('score')}")
    print(f"Reason: {event.get('reason')}")
    print(f"Suggested comment: {event.get('suggested_comment')}")


def main():
    #  Định nghĩa danh sách các từ khóa cần tìm kiếm
    keywords = ["AI", "Recruiting", "Startup", "HR", "SaaS", "Fintech"]

    # meetup_events = crawl_meetup(keywords)

    # for event in meetup_events:

    #     process_event(event)

    # print(f"\n🎉 TỔNG SỐ EVENTS MEETUP TÌM ĐƯỢC: {len(meetup_events)}")

    youtube_live_events = crawl_youtube_live(keywords)

    for event in youtube_live_events:
        process_event(event)

    print(f"\n🎉 TỔNG SỐ EVENTS YOUTUBE LIVE TÌM ĐƯỢC: {len(youtube_live_events)}")


if __name__ == "__main__":
    main()
