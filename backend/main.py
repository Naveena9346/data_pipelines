from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.db import async_engine, Base, AsyncSessionLocal
from app.api.v1.router import api_router
from app.scripts.seed_db import seed_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables on startup
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed initial roles and operational data
    await seed_data()

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": f"{settings.API_V1_STR}/docs"
    }
