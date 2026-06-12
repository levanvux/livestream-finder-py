from sqlalchemy import *

engine = create_engine("sqlite:///livestream.db")

metadata = MetaData()

livestreams = Table(
    "livestreams",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("platform", String),
    Column("description", Text),
    Column("url", String),
    Column("score", Integer),
    Column("industry", String),
    Column("language", String),
    Column("buyer_persona", String),
)

metadata.create_all(engine)
