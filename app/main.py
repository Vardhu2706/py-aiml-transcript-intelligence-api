from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1 import endpoints as v1_endpoints
from app.db import engine, Base
from app.utils.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up app")
    try: 
        Base.metadata.create_all(bind=engine)
        logger.info("Ensured DB tables created (metadata.create_all)")
    except Exception as e:
        logger.exception("Error creating DB tables: %s", e)
        
    yield
    
    logger.info("Shutting down app")
    
app = FastAPI(
    title="Transcript Intelligence - API",
    version="0.1.0",
    lifespan=lifespan
)

# CORS (allow local dev)
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(v1_endpoints.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {'status': 'ok'}