import streamlit as st
import pandas as pd

from src.crawler.youtube import crawl_youtube_live
from src.ai.classify import classify_event
from src.database.livestream_repository import save_event

st.set_page_config(
    page_title="Livestream Finder",
    layout="wide",
)

st.title("🎯 Tool tìm livestream có khách hàng tiềm năng và đánh giá bằng AI")

# === Search area ===

with st.form("search_form"):

    col1, col2, col3 = st.columns([1.5, 1, 1])

    with col1:
        keywords_text = st.text_area(
            "Keywords (mỗi dòng là 1 keyword)",
            value="""Charity
Tokenization
Cross-border payment""",
            height=150,
        )

    with col2:
        platform = st.selectbox(
            "Nền tảng",
            ["YouTube"],
        )

        enable_ai = st.checkbox(
            "Đánh giá bằng AI",
            value=True,
        )

    with col3:
        limit = st.number_input(
            "Số lượng",
            min_value=1,
            max_value=100,
            value=5,
        )

        st.write("")
        st.write("")

        search_btn = st.form_submit_button(
            "🔍 Tìm kiếm",
            use_container_width=True,
        )

# === Main ===

if search_btn:

    keywords = [
        keyword.strip() for keyword in keywords_text.splitlines() if keyword.strip()
    ]

    st.write("### TỪ KHÓA")

    st.write(keywords)

    # === Crawl ===
    with st.spinner("Đang lấy dữ liệu của các livestream..."):

        if platform == "YouTube":

            events = crawl_youtube_live(keywords, limit)

        else:
            events = []

    events = events[:limit]

    st.success(f"Đã tìm thấy {len(events)} livestreams")

    results = []

    progress = st.progress(0)
    status = st.empty()

    total = len(events)

    for index, event in enumerate(events):

        current = index

        if current == 0:
            status.info(f"⏳ Đang tải thông tin các livestreams...")
        else:
            status.info(f"⏳ Đã tải thông tin của {current}/{total} livestreams...")

        if enable_ai:

            ai_result = classify_event(
                event["title"],
                event.get("description", ""),
            )

            event.update(ai_result)

            try:
                save_event(event)
            except Exception:
                pass

            results.append(event)

            progress.progress((current + 1) / total)

        status.success(f"✅ Đã xử lý xong {total} livestreams")

    # === Dataframe ===

    st.write("## KẾT QUẢ")

    df = pd.DataFrame(results)

    df = df.rename(
        columns={
            "title": "Tiêu đề",
            "platform": "Nền tảng",
            "keyword": "Từ khóa",
            "industry": "Ngành nghề",
            "language": "Ngôn ngữ",
            "buyer_persona": "Đối tượng khách hàng",
            "score": "Điểm tiềm năng",
            "url": "Link",
            "suggested_comment": "Bình luận được gửi vào livestream",
        }
    )

    show_columns = [
        col
        for col in [
            "Tiêu đề",
            "Nền tảng",
            "Từ khóa",
            "Ngành nghề",
            "Ngôn ngữ",
            "Đối tượng khách hàng",
            "Điểm tiềm năng",
            "Link",
            "Bình luận được gửi vào livestream",
        ]
        if col in df.columns
    ]

    st.dataframe(
        df[show_columns],
        use_container_width=True,
    )

    # === Detail View ===

    st.write("## CHI TIẾT")

    for event in results:

        with st.expander(
            f"{event.get('title')} | Điểm tiềm năng: {event.get('score')}/100"
        ):

            st.write(f"**Nền tảng:** {event.get('platform')}")

            st.write(f"**Từ khóa:** {event.get('keyword')}")

            st.write(f"**Ngành nghề:** {event.get('industry')}")

            st.write(f"**Điểm tiềm năng:** {event.get('score')}")

            st.write(f"**Ngôn ngữ:** {event.get('language')}")

            st.write(f"**Đối tượng khách hàng:** {event.get('buyer_persona')}")

            st.write(f"**Lý do đánh giá từ AI:** {event.get('reason')}")

            st.write(f"**Link livestream:** {event.get('url')}")

            st.write(
                f"**Bình luận được gửi vào livestream:** {event.get('suggested_comment')}"
            )
