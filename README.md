<div align="center">

# 💬 AI Chatbot FastAPI

**A production-ready multi-provider AI chatbot with streaming responses, authentication & conversation management**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![Google Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation)

</div>

---

## 📌 Overview

A **production-grade AI chatbot backend** built with FastAPI that supports multiple LLM providers (OpenAI, Google Gemini, Ollama). Features streaming responses via Server-Sent Events, conversation history management, JWT authentication, rate limiting, and a clean Streamlit frontend.

---

## ✨ Features

- 🤖 **Multi-Provider** — Seamlessly switch between OpenAI, Google Gemini, and Ollama
- ⚡ **Streaming Responses** — Real-time token streaming via SSE (Server-Sent Events)
- 💬 **Conversation Management** — Full history with create, list, delete operations
- 🔐 **JWT Authentication** — Secure API access with token-based auth
- 🚦 **Rate Limiting** — Token bucket rate limiting per user
- 🔄 **System Prompts** — Customizable per-conversation system prompts
- 📊 **Token Counting** — Track usage and costs per conversation
- 🎨 **Streamlit Frontend** — Clean, responsive chat interface
- 🐳 **Docker Ready** — Docker Compose for easy deployment
- 📝 **OpenAPI Docs** — Auto-generated interactive API documentation

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────┐
│                 Streamlit Frontend                    │
│    Chat UI │ Provider Selector │ Conversation List    │
└──────────────────────┬───────────────────────────────┘
                       │ HTTP / SSE
┌──────────────────────▼───────────────────────────────┐
│                  FastAPI Backend                      │
│  ┌──────────┐ ┌──────────┐ ┌───────────────────────┐ │
│  │  Auth    │ │  Rate    │ │  Conversation          │ │
│  │  Layer   │ │  Limiter │ │  Manager              │ │
│  └────┬─────┘ └────┬─────┘ └───────────┬───────────┘ │
│       └─────────────┴─────────────┬────┘             │
│                                   ▼                  │
│  ┌────────────────────────────────────────────────┐  │
│  │            LLM Provider Router                 │  │
│  │   OpenAI  │   Gemini   │   Ollama (local)     │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/altafpinjari2001/ai-chatbot-fastapi.git
cd ai-chatbot-fastapi

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add your API keys

# Start the backend
uvicorn src.app:app --reload --port 8000

# Start the frontend (new terminal)
streamlit run frontend/app.py
```

---

## 📖 API Documentation

Interactive API docs available at: `http://localhost:8000/docs`

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Get JWT access token |
| `POST` | `/chat` | Send message & get response |
| `POST` | `/chat/stream` | Stream response via SSE |
| `GET` | `/conversations` | List all conversations |
| `POST` | `/conversations` | Create new conversation |
| `DELETE` | `/conversations/{id}` | Delete a conversation |

### Example: Streaming Chat

```python
import httpx

async with httpx.AsyncClient() as client:
    async with client.stream(
        "POST",
        "http://localhost:8000/chat/stream",
        json={
            "message": "Explain transformers in AI",
            "conversation_id": "conv-123",
            "provider": "openai",
            "model": "gpt-4o-mini",
        },
        headers={"Authorization": "Bearer <token>"},
    ) as response:
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                print(line[6:], end="", flush=True)
```

---

## 📁 Project Structure

```
ai-chatbot-fastapi/
├── src/
│   ├── __init__.py
│   ├── app.py                 # FastAPI application
│   ├── config.py              # Settings management
│   ├── auth/
│   │   ├── jwt_handler.py     # JWT token management
│   │   ├── routes.py          # Auth endpoints
│   │   └── models.py          # User models
│   ├── chat/
│   │   ├── routes.py          # Chat endpoints
│   │   ├── schemas.py         # Request/response schemas
│   │   └── service.py         # Chat business logic
│   ├── providers/
│   │   ├── base.py            # Abstract provider interface
│   │   ├── openai_provider.py # OpenAI integration
│   │   ├── gemini_provider.py # Gemini integration
│   │   └── ollama_provider.py # Ollama integration
│   ├── conversations/
│   │   ├── manager.py         # Conversation CRUD
│   │   └── models.py          # Conversation schemas
│   └── middleware/
│       └── rate_limiter.py    # Rate limiting
├── frontend/
│   └── app.py                 # Streamlit chat UI
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── tests/
├── .github/workflows/ci.yml
├── LICENSE
└── .gitignore
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

<div align="center"><b>⭐ Star this repo if you find it useful!</b></div>
