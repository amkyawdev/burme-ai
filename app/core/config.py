"""
Burme AI Platform Configuration
Manages API keys and environment variables
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application Settings"""
    
    # App Info
    APP_NAME = "Burme AI Platform"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "AI-Powered Platform for Chat, Image, Video, App, Song & Story Generation"
    
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    
    # Cloudflare AI
    CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
    CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # PixVerse API
    PIXVERSE_API_KEY = os.getenv("PIXVERSE_API_KEY", "")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "burme-ai-secret-key-change-in-production")
    
    # CORS
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]


settings = Settings()