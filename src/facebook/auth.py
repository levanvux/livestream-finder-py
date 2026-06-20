from pathlib import Path
from playwright.sync_api import sync_playwright

STATE_FILE = Path(__file__).parent / "facebook_state.json"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.facebook.com")

    input("Đăng nhập xong rồi nhấn Enter...")

    context.storage_state(path=str(STATE_FILE))

    print(f"Saved state to: {STATE_FILE}")

    browser.close()
