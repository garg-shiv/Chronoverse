from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from contextlib import asynccontextmanager

from .api.dialogue import router as dialogue_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting Chronoverse Backend...")
    
    os.makedirs("generated_audio", exist_ok=True)
    logger.info("📁 Audio directory ready")
    
    yield
    
    logger.info("⏹️ Shutting down Chronoverse Backend")

app = FastAPI(
    title="Chronoverse API",
    description="AI-powered historical education platform with voice interaction",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/audio", StaticFiles(directory="generated_audio"), name="audio")

app.include_router(dialogue_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Chronoverse Historical Education API",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "chronoverse-backend",
        "version": "1.0.0"
    }
