from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session
from typing import List
from app.core.database import get_session
from app.crud.link import crud_link
from app.schemas.link import LinkCreate, LinkUpdate, LinkResponse
from app.models.link import Link

router = APIRouter()

@router.get("/links", response_model=List[LinkResponse])
def read_links(
    range: str = Query(default="[0,10]", description="Range in format [start,end]"),
    db: Session = Depends(get_session),
):
    try:
        range_values = range.strip("[]").split(",")
        start = int(range_values[0])
        end = int(range_values[1])
    except Exception:
        start, end = 0, 10
    
    if start < 0 or end <= start:
        start, end = 0, 10
    
    limit = end - start
    links = crud_link.get_multi(db, skip=start, limit=limit)
    total = crud_link.get_total_count(db)
    
    response_links = []
    for link in links:
        link_data = LinkResponse.from_orm(link)
        response_links.append(link_data)
    
    return response_links

@router.post("/links", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
def create_link(link: LinkCreate, db: Session = Depends(get_session)):
    existing = crud_link.get_by_short_name(db, link.short_name)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Short name already exists"
        )
    
    db_link = crud_link.create(db, link)
    return LinkResponse.from_orm(db_link)

@router.get("/links/{link_id}", response_model=LinkResponse)
def read_link(link_id: int, db: Session = Depends(get_session)):
    db_link = crud_link.get(db, link_id)
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    return LinkResponse.from_orm(db_link)

@router.put("/links/{link_id}", response_model=LinkResponse)
def update_link(
    link_id: int, 
    link: LinkUpdate, 
    db: Session = Depends(get_session)
):
    db_link = crud_link.get(db, link_id)
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    if link.short_name != db_link.short_name:
        existing = crud_link.get_by_short_name(db, link.short_name)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Short name already exists"
            )
    
    updated_link = crud_link.update(db, db_link, link)
    return LinkResponse.from_orm(updated_link)

@router.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(link_id: int, db: Session = Depends(get_session)):
    db_link = crud_link.get(db, link_id)
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    crud_link.delete(db, link_id)
    return None

@router.get("/r/{short_name}")
def redirect_to_original(short_name: str, db: Session = Depends(get_session)):
    db_link = crud_link.get_by_short_name(db, short_name)
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=str(db_link.original_url))
