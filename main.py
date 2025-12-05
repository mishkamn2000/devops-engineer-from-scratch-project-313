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
