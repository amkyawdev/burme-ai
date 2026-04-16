"""
Chat API - Llama-3 Integration
Handles chat requests using Cloudflare AI Workers
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
import aiohttp
import json

from app.core.config import settings

router = APIRouter(prefix="/api/chat", tags=["Chat"])


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    response: str
    model: str = "llama-3"


async def call_cloudflare_ai(prompt: str, history: List[dict] = None) -> str:
    """Call Cloudflare AI Workers with Llama-3 model"""
    if not settings.CLOUDFLARE_ACCOUNT_ID or not settings.CLOUDFLARE_API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cloudflare API credentials not configured"
        )
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/meta/llama-3-8b-chat"
    
    headers = {
        "Authorization": f"Bearer {settings.CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Build messages with history
    messages = []
    if history:
        for msg in history:
            messages.append({"role": msg.get("role"), "content": msg.get("content")})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "messages": messages
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("result", {}).get("response", "No response from AI")
            else:
                error = await response.text()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Cloudflare AI Error: {error}"
                )


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with Llama-3 AI"""
    try:
        history_dict = [{"role": msg.role, "content": msg.content} for msg in request.history]
        response = await call_cloudflare_ai(request.message, history_dict)
        return ChatResponse(response=response)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/models")
async def get_available_models():
    """Get available chat models"""
    return {
        "models": [
            {"id": "llama-3", "name": "Llama 3", "provider": "Cloudflare"},
            {"id": "mistral-7b", "name": "Mistral 7B", "provider": "Cloudflare"},
        ]
    }