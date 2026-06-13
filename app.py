from crawler.meetup import crawl_meetup
from crawler.youtube import crawl_youtube_live


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

        print("-" * 50)

        print(f"Title: {event['title']}")

        print(f"Platform: {event['platform']}")

        print(f"URL: {event['url']}")

        print(f"description: {event['description']}")

        print(f"Keyword: {event['keyword']}")

    print(f"\n🎉 TỔNG SỐ EVENTS YOUTUBE LIVE TÌM ĐƯỢC: {len(youtube_live_events)}")


if __name__ == "__main__":
    main()
