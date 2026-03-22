"""Configuration."""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    gemini_api_key: str = Field(default="", env="GEMINI_API_KEY")
    jwt_secret: str = Field(default="change-me-in-production", env="JWT_SECRET")

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
