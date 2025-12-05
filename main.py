import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn.access")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed_ms = (time.time() - start) * 1000
    logger.info(f"{request.method} {request.url.path} completed_in={elapsed_ms:.2f}ms status_code={response.status_code}")
    return response

@app.get("/ping")
async def ping():
    return "pong"

import os
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN)
    app.add_middleware(SentryAsgiMiddleware)

@app.get("/error")
async def trigger_error():
    raise RuntimeError("Test Sentry error")

from fastapi import HTTPException, Depends
from sqlmodel import Session
from app.db.session import init_db, get_session
from app.crud.link_crud import list_links, get_link, create_link, update_link, delete_link, BASE_URL
from app.models.link import Link

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/api/links")
def api_list_links(session: Session = Depends(get_session)):
    links = list_links(session)
    return [{"id": l.id, "original_url": l.original_url, "short_name": l.short_name, "short_url": f"{BASE_URL}/{l.short_name}"} for l in links]

@app.post("/api/links", status_code=201)
def api_create_link(link: Link, session: Session = Depends(get_session)):
    try:
        new_link = create_link(session, link.original_url, link.short_name)
        return {"id": new_link.id, "original_url": new_link.original_url, "short_name": new_link.short_name, "short_url": f"{BASE_URL}/{new_link.short_name}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/links/{link_id}")
def api_get_link(link_id: int, session: Session = Depends(get_session)):
    link = get_link(session, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"id": link.id, "original_url": link.original_url, "short_name": link.short_name, "short_url": f"{BASE_URL}/{link.short_name}"}

@app.put("/api/links/{link_id}")
def api_update_link(link_id: int, link_data: Link, session: Session = Depends(get_session)):
    updated = update_link(session, link_id, link_data.original_url, link_data.short_name)
    if not updated:
        raise HTTPException(status_code=404, detail="Link not found")
    return {"id": updated.id, "original_url": updated.original_url, "short_name": updated.short_name, "short_url": f"{BASE_URL}/{updated.short_name}"}

@app.delete("/api/links/{link_id}", status_code=204)
def api_delete_link(link_id: int, session: Session = Depends(get_session)):
    success = delete_link(session, link_id)
    if not success:
        raise HTTPException(status_code=404, detail="Link not found")

from fastapi import Query, Response

@app.get("/api/links")
def api_list_links_paginated(response: Response, range: str = Query("[0,10]"), session: Session = Depends(get_session)):
    import json, re
    m = re.match(r"\[(\d+),\s*(\d+)\]", range)
    start, end = (0, 10)
    if m:
        start, end = int(m.group(1)), int(m.group(2))
    links = list_links(session)
    total = len(links)
    paginated_links = links[start:end]
    response.headers["Content-Range"] = f"links {start}-{min(end, total)}/{total}"
    return [{"id": l.id, "original_url": l.original_url, "short_name": l.short_name, "short_url": f"{BASE_URL}/{l.short_name}"} for l in paginated_links]

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
