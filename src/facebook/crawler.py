from playwright.sync_api import sync_playwright
from pathlib import Path
import json


def on_response(response):
    if "graphql" not in response.url.lower():
        return

    try:
        request = response.request

        if (
            request.post_data
            and "CometVideoHomeLiveSectionsListPaginationQuery" in request.post_data
        ):
            body = response.text()

            for line in body.splitlines():
                line = line.strip()

                if not line:
                    continue

                try:
                    obj = json.loads(line)
                    print(obj.keys())
                except:
                    pass

    except Exception as e:
        print("Response error:", e)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        storage_state=Path(__file__).with_name("facebook_state.json")
    )

    context.on("response", on_response)

    page = context.new_page()

    page.goto("https://facebook.com/watch/live")

    page.wait_for_timeout(15000)

    input("Enter to close...")

    browser.close()
