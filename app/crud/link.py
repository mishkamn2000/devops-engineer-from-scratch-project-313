from sqlmodel import Session, select
from typing import List, Optional
from app.models.link import Link
from app.schemas.link import LinkCreate, LinkUpdate

class CRUDLink:
    @staticmethod
    def get(db: Session, id: int) -> Optional[Link]:
        return db.get(Link, id)
    
    @staticmethod
    def get_by_short_name(db: Session, short_name: str) -> Optional[Link]:
        statement = select(Link).where(Link.short_name == short_name)
        return db.exec(statement).first()
    
    @staticmethod
    def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Link]:
        statement = select(Link).offset(skip).limit(limit)
        return db.exec(statement).all()
    
    @staticmethod
    def get_total_count(db: Session) -> int:
        statement = select(Link)
        return len(db.exec(statement).all())
    
    @staticmethod
    def create(db: Session, obj_in: LinkCreate) -> Link:
        db_obj = Link(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    def update(db: Session, db_obj: Link, obj_in: LinkUpdate) -> Link:
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    @staticmethod
    def delete(db: Session, id: int) -> None:
        obj = db.get(Link, id)
        if obj:
            db.delete(obj)
            db.commit()

crud_link = CRUDLink()
