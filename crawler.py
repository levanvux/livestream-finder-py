import time
import requests
from bs4 import BeautifulSoup

# 1. Định nghĩa danh sách các từ khóa cần tìm kiếm
keywords = ["AI", "Recruiting", "Startup", "HR", "SaaS", "Fintech"]

# Giả lập trình duyệt
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 2. Vòng lặp duyệt qua từng từ khóa trong danh sách
for keyword in keywords:
    print(f"\nĐANG TÌM KIẾM VỚI TỪ KHÓA: '{keyword.upper()}'...")
    print("=" * 60)

    url = f"https://www.meetup.com/find/?keywords={keyword}"

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Tìm các Event Card
            event_cards = soup.find_all("a", {"data-event-label": "Event Card"})
            total_events = len(event_cards)

            print(f"🎉 Từ khóa '{keyword}': Tìm thấy {total_events} sự kiện!\n")

            for index, event in enumerate(event_cards, start=1):
                try:
                    # Lấy Tiêu đề
                    title = (
                        event.find("h3").text.strip()
                        if event.find("h3")
                        else "Không có tiêu đề"
                    )

                    # Lấy Link sự kiện
                    event_url = event.get("href")

                    # Lấy Thời gian
                    time_tag = event.find("time")
                    event_time = time_tag.text.strip() if time_tag else "N/A"

                    # Lấy Đơn vị tổ chức
                    organizer_tag = event.find(
                        "div", class_="flex-shrink min-w-0 truncate"
                    )
                    organizer = (
                        organizer_tag.text.replace("by", "").strip()
                        if organizer_tag
                        else "N/A"
                    )

                    # Lấy Số chỗ còn lại
                    seats_left_tag = event.find(
                        lambda tag: tag.name == "span" and "seats left" in tag.text
                    )
                    seats_left = (
                        seats_left_tag.text.strip()
                        if seats_left_tag
                        else "Còn chỗ/Không giới hạn"
                    )

                    # Lấy Số người tham gia
                    attendees_tag = event.find(
                        lambda tag: tag.name == "span" and "attendees" in tag.text
                    )
                    attendees = (
                        attendees_tag.text.strip() if attendees_tag else "0 attendees"
                    )

                    # LOG RA TERMINAL
                    print(f"[{index}/{total_events}] 📌 TIÊU ĐỀ: {title}")
                    print(f"    🔗 Đường dẫn: {event_url}")
                    print(f"    ⏰ Thời gian: {event_time}")
                    print(f"    👤 Tổ chức:   {organizer}")
                    print(f"    🎟️ Trạng thái: {seats_left}")
                    print(f"    👥 Tham gia:  {attendees}")
                    print("-" * 50)
                except Exception as e:
                    print(f"❌ Lỗi khi đọc thông tin sự kiện thứ {index}: {e}")

        else:
            # Nếu không thể lấy dữ liệu cho từ khóa
            print(
                f"❌ Không thể lấy dữ liệu cho từ khóa '{keyword}'. Mã lỗi từ hệ thống Meetup: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        print(f"💥 Đã xảy ra lỗi kết nối khi tìm từ khóa '{keyword}': {e}")

    # Nghỉ 2 giây trước khi chuyển sang từ khóa tiếp theo để tránh hệ thống chống bot
    time.sleep(2)

print("\nHOÀN THÀNH QUÁ TRÌNH QUÉT TẤT CẢ TỪ KHÓA!")
