"""
AI Chatbot - OpenAI Provider.

Integration with OpenAI's chat completion API.
"""

import logging
from typing import AsyncIterator

from openai import AsyncOpenAI

from .base import BaseLLMProvider, ChatMessage, ChatResponse

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider."""

    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.default_model = "gpt-4o-mini"

    async def generate(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> ChatResponse:
        """Generate a complete response from OpenAI."""
        response = await self.client.chat.completions.create(
            model=model or self.default_model,
            messages=[
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        choice = response.choices[0]
        return ChatResponse(
            content=choice.message.content or "",
            model=response.model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            } if response.usage else None,
        )

    async def stream(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncIterator[str]:
        """Stream response tokens from OpenAI."""
        stream = await self.client.chat.completions.create(
            model=model or self.default_model,
            messages=[
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )

        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content
