from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from app.api.links import router as links_router
from app.core.config import settings
from app.core.database import engine
from app.models.link import SQLModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[FastApiIntegration(), SqlalchemyIntegration()],
            traces_sample_rate=1.0,
        )
    
    SQLModel.metadata.create_all(engine)
    yield
    engine.dispose()

app = FastAPI(
    title="URL Shortener",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(links_router, prefix="/api")

@app.get("/ping")
def ping():
    return "pong"

@app.get("/health")
def health():
    return {"status": "healthy"}
