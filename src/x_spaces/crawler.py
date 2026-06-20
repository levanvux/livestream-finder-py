from playwright.sync_api import sync_playwright
from pathlib import Path
from urllib.parse import quote


def extract_space(result, keyword=None):

    try:
        card = result["card"]["legacy"]

        if card["name"] != "3691233323:audiospace":
            return None

        space_id = next(
            item["value"]["string_value"]
            for item in card["binding_values"]
            if item["key"] == "id"
        )

        user = result["core"]["user_results"]["result"]

        host_name = user["core"]["name"]
        host_username = user["core"]["screen_name"]

        tweet_text = result["legacy"]["full_text"]

        return {
            "title": f"X Space by {host_name}",
            "platform": "X Spaces",
            "url": f"https://x.com/i/spaces/{space_id}",
            "description": tweet_text,
            "keyword": keyword,
            "start_time": result["legacy"]["created_at"],
            "space_id": space_id,
            "host_name": host_name,
            "host_username": host_username,
            "views": result.get("views", {}).get("count", "0"),
        }

    except Exception:
        return None


def crawl_x_spaces(keywords, limit=3):

    events = []

    def on_response(response):

        if "/graphql/" not in response.url:
            return

        try:
            data = response.json()
        except Exception:
            return

        if "search_by_raw_query" not in data.get("data", {}):
            return

        try:

            entries = data["data"]["search_by_raw_query"]["search_timeline"][
                "timeline"
            ]["instructions"][0]["entries"]

            for entry in entries:

                try:

                    result = entry["content"]["itemContent"]["tweet_results"]["result"]

                    space = extract_space(
                        result,
                        keyword=current_keyword,
                    )

                    if space:
                        events.append(space)

                except Exception:
                    continue

        except Exception:
            pass

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            storage_state=Path(__file__).with_name("x_state.json")
        )

        page = context.new_page()

        page.on("response", on_response)

        for keyword in keywords:

            global current_keyword
            current_keyword = keyword

            before = len(events)

            page.goto(
                f"https://x.com/search?q={quote(f'filter:spaces {keyword}')}&src=typed_query&f=live"
            )

            page.wait_for_timeout(5000)

            after = len(events)

            if after - before > limit:
                del events[before + limit : after]

        browser.close()

    return events
