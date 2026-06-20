from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://x.com/login")

    print("Đăng nhập xong thì Enter...")

    input()

    page.context.storage_state(path="storage_state.json")

    browser.close()
