"""
AI Chatbot - Chat Routes.

API endpoints for chat operations with streaming support.
"""

import logging
from typing import AsyncIterator

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ..providers.base import ChatMessage
from ..providers.openai_provider import OpenAIProvider
from ..providers.gemini_provider import GeminiProvider
from ..config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter()


class ChatRequest(BaseModel):
    """Chat request schema."""
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: str | None = None
    provider: str = Field(default="openai")
    model: str | None = None
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=2048, ge=1, le=8192)
    system_prompt: str | None = None


class ChatResponse(BaseModel):
    """Chat response schema."""
    response: str
    conversation_id: str
    model: str
    usage: dict | None = None


def get_provider(provider_name: str):
    """Get the appropriate LLM provider."""
    settings = get_settings()

    if provider_name == "openai":
        return OpenAIProvider(api_key=settings.openai_api_key)
    elif provider_name == "gemini":
        return GeminiProvider(api_key=settings.gemini_api_key)
    else:
        raise HTTPException(
            400, f"Unsupported provider: {provider_name}"
        )


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    """Send a message and get a complete response."""
    provider = get_provider(request.provider)
    conv_manager = req.app.state.conversation_manager

    # Get or create conversation
    conv_id = request.conversation_id or conv_manager.create()
    history = conv_manager.get_history(conv_id)

    # Build messages
    messages = []
    if request.system_prompt:
        messages.append(
            ChatMessage(role="system", content=request.system_prompt)
        )
    messages.extend(history)
    messages.append(
        ChatMessage(role="user", content=request.message)
    )

    # Generate response
    response = await provider.generate(
        messages=messages,
        model=request.model,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    # Save to history
    conv_manager.add_message(conv_id, "user", request.message)
    conv_manager.add_message(conv_id, "assistant", response.content)

    return ChatResponse(
        response=response.content,
        conversation_id=conv_id,
        model=response.model,
        usage=response.usage,
    )


@router.post("/stream")
async def chat_stream(request: ChatRequest, req: Request):
    """Stream a chat response via Server-Sent Events."""
    provider = get_provider(request.provider)

    messages = []
    if request.system_prompt:
        messages.append(
            ChatMessage(role="system", content=request.system_prompt)
        )
    messages.append(
        ChatMessage(role="user", content=request.message)
    )

    async def event_generator() -> AsyncIterator[str]:
        full_response = ""
        async for token in provider.stream(
            messages=messages,
            model=request.model,
            temperature=request.temperature,
        ):
            full_response += token
            yield f"data: {token}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
