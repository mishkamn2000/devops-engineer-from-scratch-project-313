from sqlmodel import create_engine, Session
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL or "sqlite:///./test.db",
    echo=True,
    connect_args={"check_same_thread": False} if "sqlite" in (settings.DATABASE_URL or "") else {}
)

def get_session():
    with Session(engine) as session:
        yield session
