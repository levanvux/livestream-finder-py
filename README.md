# Lead Discovery

Find high-potential livestreams, webinars, and events.

Features:

- Crawl livestream/event data
- AI classification
- Opportunity scoring
- Engagement suggestions

---

## Cách chạy project để tìm live trên TWITCH

1. Tạo tài khoản Twitch -> Xác thực Two-Factor -> Truy cập vào https://dev.twitch.tv/docs/api/ -> Login -> Tạo APP -> Lấy client_id và client_secret của APP

2. Tạo file .env trong project, sau đó thêm vào 2 biến:

```bash
TWITCH_CLIENT_ID=<client_id ở bước trên>
TWITCH_CLIENT_SECRET=<client_secret ở bước trên>
```

3. Chạy file twitch/auth.py để tạo Access Token:

```bash
python -m src.twitch.auth
```

3. Chạy file twitch/crawler.py để lấy live:

```bash
python -m src.twitch.crawler
```

---

- Hiện tại link https://livestreamradar.streamlit.app không hoạt động được, đang trong quá trình xây dựng.
