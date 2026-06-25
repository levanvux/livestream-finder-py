from src.ai.classify import classify_event
from src.database.livestream_repository import save_event
from src.youtube.livechat import get_live_chat_id, send_message


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


def print_event(event: dict):
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


def process_event(event: dict):
    classify_result = classify_event(
        event["title"],
        event.get("description", ""),
    )

    event.update(classify_result)

    # if event.get("score") >= 70:
    #     save_event(event)

    # try_comment(event)
    print_event(event)


def process_events(events: list[dict]):
    for event in events:
        process_event(event)
