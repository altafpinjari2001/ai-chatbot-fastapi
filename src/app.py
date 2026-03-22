"""
AI Chatbot FastAPI - Main Application.

Production-ready chatbot API with multi-provider LLM support.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .auth.routes import router as auth_router
from .chat.routes import router as chat_router
from .conversations.manager import ConversationManager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    logger.info("🚀 AI Chatbot API starting up...")
    app.state.conversation_manager = ConversationManager()
    yield
    logger.info("🛑 AI Chatbot API shutting down...")


app = FastAPI(
    title="AI Chatbot API",
    description="Multi-provider AI chatbot with streaming responses",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
