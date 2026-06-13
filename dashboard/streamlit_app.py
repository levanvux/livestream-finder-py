import streamlit as st
import pandas as pd

from crawler.youtube import crawl_youtube_live
from ai.classify import classify_event
from database.livestream_repository import save_event

st.set_page_config(
    page_title="Livestream Finder",
    layout="wide",
)

st.title("🎯 Livestream Finder")
st.write("Tìm livestream có khách hàng tiềm năng và đánh giá bằng AI.")

# === Sidebar ===

st.sidebar.header("Search Options")

platform = st.sidebar.selectbox(
    "Platform",
    [
        "YouTube",
    ],
)

keywords_text = st.sidebar.text_area(
    "Keywords (mỗi dòng là 1 keyword)",
    value="""AI
Recruiting
Startup
HR
SaaS
Fintech""",
)

enable_ai = st.sidebar.checkbox(
    "AI Classification",
    value=True,
)

limit = st.sidebar.number_input(
    "Max Results",
    min_value=1,
    max_value=100,
    value=20,
)

search_btn = st.sidebar.button("Search Livestreams")

# === Main ===

if search_btn:

    keywords = [
        keyword.strip() for keyword in keywords_text.splitlines() if keyword.strip()
    ]

    st.write("### Keywords")

    st.write(keywords)

    # === Crawl ===
    with st.spinner("Crawling livestreams..."):

        if platform == "YouTube":

            events = crawl_youtube_live(keywords)

        else:
            events = []

    events = events[:limit]

    st.success(f"Found {len(events)} livestreams")

    results = []

    progress = st.progress(0)

    for index, event in enumerate(events):

        if enable_ai:

            ai_result = classify_event(
                event["title"],
                event.get(
                    "description",
                    "",
                ),
            )

            event.update(ai_result)

        try:
            save_event(event)

        except Exception:
            pass

        results.append(event)

        progress.progress((index + 1) / len(events))

    # === Dataframe ===

    st.write("## Results")

    df = pd.DataFrame(results)

    show_columns = [
        col
        for col in [
            "title",
            "platform",
            "keyword",
            "industry",
            "language",
            "buyer_persona",
            "score",
            "url",
        ]
        if col in df.columns
    ]

    st.dataframe(
        df[show_columns],
        use_container_width=True,
    )

    # === Detail View ===

    st.write("## Livestream Details")

    for event in results:

        with st.expander(f"{event.get('title')} | Score: {event.get('score', 0)}"):

            st.write(f"**Platform:** {event.get('platform')}")

            st.write(f"**Keyword:** {event.get('keyword')}")

            st.write(f"**Industry:** {event.get('industry')}")

            st.write(f"**Language:** {event.get('language')}")

            st.write(f"**Buyer Persona:** {event.get('buyer_persona')}")

            st.write(f"**Score:** {event.get('score')}")

            st.write(f"**Reason:** {event.get('reason')}")

            st.write(f"**URL:** {event.get('url')}")
