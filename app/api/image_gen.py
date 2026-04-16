"""
Image Generation API - Stable Diffusion / DALL-E Integration
Handles image generation requests
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import aiohttp

from app.core.config import settings

router = APIRouter(prefix="/api/image", tags=["Image Generation"])


class ImageGenerationRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = ""
    width: Optional[int] = 1024
    height: Optional[int] = 1024
    num_images: Optional[int] = 1


class ImageGenerationResponse(BaseModel):
    images: list[str]
    model: str = "stable-diffusion"


async def generate_with_dalle(prompt: str, num_images: int = 1) -> list[str]:
    """Generate images using OpenAI DALL-E"""
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI API key not configured"
        )
    
    images = []
    for _ in range(num_images):
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    image_url = result.get("data", [{}])[0].get("url", "")
                    images.append(image_url)
                else:
                    error = await response.text()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"DALL-E API Error: {error}"
                    )
    
    return images


async def generate_with_cloudflare(prompt: str) -> list[str]:
    """Generate images using Cloudflare AI Workers"""
    if not settings.CLOUDFLARE_ACCOUNT_ID or not settings.CLOUDFLARE_API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cloudflare API credentials not configured"
        )
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0"
    
    headers = {
        "Authorization": f"Bearer {settings.CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                image_data = result.get("result", {}).get("image", "")
                return [f"data:image/png;base64,{image_data}"]
            else:
                error = await response.text()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Cloudflare AI Error: {error}"
                )


@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """Generate images from text prompt"""
    try:
        # Try Cloudflare first, fall back to DALL-E
        if settings.CLOUDFLARE_ACCOUNT_ID and settings.CLOUDFLARE_API_TOKEN:
            images = await generate_with_cloudflare(request.prompt)
        elif settings.OPENAI_API_KEY:
            images = await generate_with_dalle(request.prompt, request.num_images)
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No AI image generation service configured"
            )
        
        return ImageGenerationResponse(images=images)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/models")
async def get_available_models():
    """Get available image generation models"""
    return {
        "models": [
            {"id": "stable-diffusion-xl", "name": "Stable Diffusion XL", "provider": "Cloudflare"},
            {"id": "dall-e-3", "name": "DALL-E 3", "provider": "OpenAI"},
        ]
    }