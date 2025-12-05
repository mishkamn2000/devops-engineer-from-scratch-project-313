from sqlmodel import select
from app.models.link import Link
from app.db.session import get_session

BASE_URL = os.getenv("BASE_URL", "https://short.io/r")

def list_links(session):
    return session.exec(select(Link)).all()

def get_link(session, link_id: int):
    return session.get(Link, link_id)

def create_link(session, original_url: str, short_name: str):
    link = Link(original_url=original_url, short_name=short_name)
    session.add(link)
    session.commit()
    session.refresh(link)
    return link

def update_link(session, link_id: int, original_url: str, short_name: str):
    link = session.get(Link, link_id)
    if not link:
        return None
    link.original_url = original_url
    link.short_name = short_name
    session.add(link)
    session.commit()
    session.refresh(link)
    return link

def delete_link(session, link_id: int):
    link = session.get(Link, link_id)
    if not link:
        return False
    session.delete(link)
    session.commit()
    return True
