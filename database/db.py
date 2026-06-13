from sqlalchemy import *

engine = create_engine("sqlite:///livestream.db")

metadata = MetaData()

livestreams = Table(
    "livestreams",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("platform", String),
    Column("description", Text),
    Column("url", String, unique=True),
    Column("keyword", String),
    Column("start_time", DateTime),
    Column("score", Integer, default=0),
    Column("industry", String),
    Column("language", String),
    Column("buyer_persona", String),
    Column("suggested_comment", Text),
    Column("created_at", DateTime, server_default=func.now()),
)

metadata.create_all(engine)
