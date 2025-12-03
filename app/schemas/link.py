from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class LinkBase(BaseModel):
    original_url: HttpUrl
    short_name: str

class LinkCreate(LinkBase):
    pass

class LinkUpdate(LinkBase):
    pass

class LinkResponse(LinkBase):
    id: int
    short_url: str
    created_at: datetime
    
    class Config:
        from_attributes = True
