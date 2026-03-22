"""
AI Chatbot - Google Gemini Provider.

Integration with Google's Gemini API.
"""

import logging
from typing import AsyncIterator

import google.generativeai as genai

from .base import BaseLLMProvider, ChatMessage, ChatResponse

logger = logging.getLogger(__name__)


class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider."""

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.default_model = "gemini-2.0-flash"

    def _convert_messages(
        self, messages: list[ChatMessage]
    ) -> tuple[str | None, list[dict]]:
        """Convert ChatMessage list to Gemini format."""
        system_prompt = None
        history = []

        for msg in messages:
            if msg.role == "system":
                system_prompt = msg.content
            else:
                role = "user" if msg.role == "user" else "model"
                history.append({
                    "role": role,
                    "parts": [msg.content],
                })
        return system_prompt, history

    async def generate(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> ChatResponse:
        """Generate a complete response from Gemini."""
        system_prompt, history = self._convert_messages(messages)

        gen_model = genai.GenerativeModel(
            model_name=model or self.default_model,
            system_instruction=system_prompt,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
        )

        # Use last user message, rest as history
        chat = gen_model.start_chat(history=history[:-1])
        response = chat.send_message(history[-1]["parts"][0])

        return ChatResponse(
            content=response.text,
            model=model or self.default_model,
        )

    async def stream(
        self,
        messages: list[ChatMessage],
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncIterator[str]:
        """Stream response tokens from Gemini."""
        system_prompt, history = self._convert_messages(messages)

        gen_model = genai.GenerativeModel(
            model_name=model or self.default_model,
            system_instruction=system_prompt,
            generation_config=genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
        )

        chat = gen_model.start_chat(history=history[:-1])
        response = chat.send_message(
            history[-1]["parts"][0], stream=True
        )

        for chunk in response:
            if chunk.text:
                yield chunk.text
