from sqlalchemy import insert, select, update, delete

from database.db import engine, livestreams


def save_event(event: dict):
    """
    Lưu 1 livestream vào database
    """

    with engine.begin() as conn:

        stmt = insert(livestreams).values(
            title=event.get("title"),
            platform=event.get("platform"),
            description=event.get("description"),
            url=event.get("url"),
            score=event.get("score", 0),
            industry=event.get("industry"),
            language=event.get("language"),
            buyer_persona=event.get("buyer_persona"),
        )

        conn.execute(stmt)


def get_all_events():
    """
    Lấy tất cả livestream
    """

    with engine.connect() as conn:

        result = conn.execute(select(livestreams))

        return result.fetchall()


def get_event_by_id(event_id: int):
    """
    Lấy livestream theo ID
    """

    with engine.connect() as conn:

        stmt = select(livestreams).where(livestreams.c.id == event_id)

        return conn.execute(stmt).fetchone()


def get_event_by_url(url: str):
    """
    Tìm livestream theo URL
    """

    with engine.connect() as conn:

        stmt = select(livestreams).where(livestreams.c.url == url)

        return conn.execute(stmt).fetchone()


def update_score(event_id: int, score: int):
    """
    Cập nhật điểm AI
    """

    with engine.begin() as conn:

        stmt = (
            update(livestreams).where(livestreams.c.id == event_id).values(score=score)
        )

        conn.execute(stmt)


def update_classification(
    event_id: int, industry: str, language: str, buyer_persona: str
):
    """
    Cập nhật kết quả phân loại AI
    """

    with engine.begin() as conn:

        stmt = (
            update(livestreams)
            .where(livestreams.c.id == event_id)
            .values(industry=industry, language=language, buyer_persona=buyer_persona)
        )

        conn.execute(stmt)


def delete_event(event_id: int):
    """
    Xóa livestream
    """

    with engine.begin() as conn:

        stmt = delete(livestreams).where(livestreams.c.id == event_id)

        conn.execute(stmt)
