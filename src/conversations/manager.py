"""
AI Chatbot - Conversation Manager.

In-memory conversation history management.
"""

import uuid
from datetime import datetime
from dataclasses import dataclass, field

from ..providers.base import ChatMessage


@dataclass
class Conversation:
    id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    messages: list[ChatMessage] = field(default_factory=list)
    title: str = "New Conversation"


class ConversationManager:
    """Manages conversation state and history."""

    def __init__(self):
        self._conversations: dict[str, Conversation] = {}

    def create(self, title: str = "New Conversation") -> str:
        conv_id = str(uuid.uuid4())
        self._conversations[conv_id] = Conversation(
            id=conv_id, title=title
        )
        return conv_id

    def get_history(self, conv_id: str) -> list[ChatMessage]:
        conv = self._conversations.get(conv_id)
        return conv.messages if conv else []

    def add_message(
        self, conv_id: str, role: str, content: str
    ) -> None:
        if conv_id not in self._conversations:
            self._conversations[conv_id] = Conversation(id=conv_id)
        self._conversations[conv_id].messages.append(
            ChatMessage(role=role, content=content)
        )

    def list_conversations(self) -> list[dict]:
        return [
            {
                "id": c.id,
                "title": c.title,
                "created_at": c.created_at.isoformat(),
                "message_count": len(c.messages),
            }
            for c in self._conversations.values()
        ]

    def delete(self, conv_id: str) -> bool:
        return self._conversations.pop(conv_id, None) is not None
