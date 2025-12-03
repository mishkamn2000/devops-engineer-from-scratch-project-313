from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Link(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    original_url: str = Field(index=True)
    short_name: str = Field(index=True, unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def short_url(self) -> str:
        from app.core.config import settings
        return f"{settings.BASE_URL}/r/{self.short_name}"
