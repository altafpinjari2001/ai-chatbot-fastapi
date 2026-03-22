"""
AI Chatbot - Auth Routes (Simplified).
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register")
async def register(username: str, password: str):
    """Register endpoint (placeholder for demo)."""
    return {"message": "User registered", "username": username}


@router.post("/login", response_model=AuthResponse)
async def login(username: str, password: str):
    """Login endpoint (placeholder for demo)."""
    return AuthResponse(
        access_token="demo-token-replace-with-jwt"
    )
