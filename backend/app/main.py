"""
=========================================================
main.py

Entry point for StadiumOS AI backend.

=========================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router as api_router
from app.websocket import router as websocket_router

app = FastAPI(
    title="StadiumOS AI",
    version="1.0.0",
    description="AI-powered Stadium Operations Platform for FIFA World Cup 2026",
)

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# ROUTES
# =========================================================

app.include_router(
    api_router,
    prefix="/api",
    tags=["API"],
)

app.include_router(
    websocket_router,
)

# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    return {
        "project": "StadiumOS AI",
        "status": "running",
        "version": "1.0.0",
    }