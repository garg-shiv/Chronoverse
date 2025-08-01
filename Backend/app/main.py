from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import logging
import signal
import sys
from datetime import datetime
from contextlib import asynccontextmanager
from pathlib import Path

from app.api.dialogue import router as dialogue_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting Chronoverse Backend...")
    logger.info("📁 Creating required directories...")
    
    os.makedirs("temp_audio", exist_ok=True)
    os.makedirs("generated_audio", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    
    logger.info("🎯 Backend ready for historical conversations!")
    
    yield
    
    logger.info("🛑 Chronoverse Backend shutting down gracefully...")

app = FastAPI(
    title="Chronoverse AI Backend",
    description="AI-powered historical character dialogue system", 
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists("generated_audio"):
    os.makedirs("generated_audio", exist_ok=True)

app.mount("/audio", StaticFiles(directory="generated_audio"), name="audio")

app.include_router(dialogue_router, prefix="/api/v1", tags=["dialogue"])

@app.get("/")
async def root():
    return {
        "message": "🏛️ Welcome to Chronoverse!",
        "status": "Backend is running successfully",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "available_endpoints": {
            "dialogue": "/api/v1/dialogue",
            "characters": "/api/v1/characters",
            "stt_info": "/api/v1/stt/info",
            "llm_info": "/api/v1/llm/info",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "chronoverse-backend",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "api": "operational",
            "stt": "ready",
            "rag": "ready",
            "llm": "ready",
            "storage": "available"
        }
    }

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

def signal_handler(sig, frame):
    logger.info("🛑 Received shutdown signal")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
if hasattr(signal, 'SIGTERM'):
    signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
        access_log=True
    )
