from src.crawler.meetup import crawl_meetup
from src.youtube.crawler import crawl_youtube_live
from src.x_spaces.crawler import crawl_x_spaces
from src.event_processor import process_events


def main():
    #  Định nghĩa danh sách các từ khóa cần tìm kiếm
    keywords = ["ChatGPT", "n8n", "AI Agent", "Cursor", "Claude", "Gemini", "LangChain"]

    # meetup_events = crawl_meetup(keywords)
    # process_events(meetup_events)
    # print(f"\n🎉 TỔNG SỐ EVENTS MEETUP TÌM ĐƯỢC: {len(meetup_events)}")

    # youtube_events = crawl_youtube_live(keywords, 3)
    # process_events(youtube_events)

    # x_events = crawl_x_spaces(keywords, 3)
    # process_events(x_events)

    # print(f"🎉 YOUTUBE: {len(youtube_events)} | X SPACES: {len(x_events)}")


if __name__ == "__main__":
    main()
