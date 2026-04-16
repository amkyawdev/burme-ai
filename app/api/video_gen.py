"""
Video Generation API - PixVerse Integration
Handles video generation requests using PixVerse API
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import aiohttp
import asyncio

from app.core.config import settings

router = APIRouter(prefix="/api/video", tags=["Video Generation"])


class VideoGenerationRequest(BaseModel):
    prompt: str
    aspect_ratio: Optional[str] = "16:9"
    negative_prompt: Optional[str] = ""


class VideoGenerationResponse(BaseModel):
    video_url: str
    task_id: str
    status: str


async def generate_with_pixverse(prompt: str, aspect_ratio: str = "16:9") -> dict:
    """Generate video using PixVerse API"""
    if not settings.PIXVERSE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="PixVerse API key not configured"
        )
    
    url = "https://api.pixverse.ai/api/v1/t2v"
    
    headers = {
        "Authorization": f"Bearer {settings.PIXVERSE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio
    }
    
    async with aiohttp.ClientSession() as session:
        # Submit generation request
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                task_id = result.get("data", {}).get("task_id", "")
                
                if not task_id:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to get task ID from PixVerse"
                    )
                
                # Poll for results
                return await poll_pixverse_result(session, url, headers, task_id)
            else:
                error = await response.text()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"PixVerse API Error: {error}"
                )


async def poll_pixverse_result(session: aiohttp.ClientSession, url: str, headers: dict, task_id: str, max_retries: int = 30) -> dict:
    """Poll PixVerse API for video generation result"""
    status_url = f"{url}/{task_id}/status"
    
    for _ in range(max_retries):
        async with session.get(status_url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                data = result.get("data", {})
                status_val = data.get("status", "")
                
                if status_val == "completed":
                    return {
                        "video_url": data.get("video_url", ""),
                        "task_id": task_id,
                        "status": "completed"
                    }
                elif status_val == "failed":
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Video generation failed"
                    )
                elif status_val == "processing":
                    await asyncio.sleep(2)
                else:
                    await asyncio.sleep(2)
            else:
                await asyncio.sleep(2)
    
    raise HTTPException(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        detail="Video generation timed out"
    )


@router.post("/generate", response_model=VideoGenerationResponse)
async def generate_video(request: VideoGenerationRequest):
    """Generate video from text prompt"""
    try:
        result = await generate_with_pixverse(request.prompt, request.aspect_ratio)
        return VideoGenerationResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/models")
async def get_available_models():
    """Get available video generation models"""
    return {
        "models": [
            {"id": "pixverse-t2v", "name": "PixVerse Text-to-Video", "provider": "PixVerse"},
        ]
    }