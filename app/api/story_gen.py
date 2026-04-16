"""
Story Generation API
Handles story generation requests using GPT-4o or Mistral-7b
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import aiohttp

from app.core.config import settings

router = APIRouter(prefix="/api/story", tags=["Story Generation"])


class StoryGenerationRequest(BaseModel):
    prompt: str
    genre: Optional[str] = "general"
    length: Optional[str] = "medium"
    style: Optional[str] = "narrative"


class StoryGenerationResponse(BaseModel):
    story: str
    title: str
    genre: str
    length: str


SYSTEM_PROMPT = """You are a Creative Story Writer AI. Your task is to generate engaging, creative stories based on user prompts.

Guidelines:
1. Create compelling narratives with clear plot, characters, and setting
2. Use descriptive language to bring scenes to life
3. Develop interesting characters with motivations
4. Build toward satisfying conclusions
5. Match the tone and style requested by the user"""



async def generate_with_mistral(prompt: str, genre: str = "general", length: str = "medium") -> dict:
    """Generate story using Cloudflare AI Workers with Mistral-7b"""
    if not settings.CLOUDFLARE_ACCOUNT_ID or not settings.CLOUDFLARE_API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Cloudflare API credentials not configured"
        )
    
    url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/meta/mistral-7b-instruct-v0.1"
    
    headers = {
        "Authorization": f"Bearer {settings.CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    length_guide = {
        "short": "a short story (500-1000 words)",
        "medium": "a medium-length story (1000-2000 words)",
        "long": "a long story (2000-5000 words)"
    }
    
    user_prompt = f"""Write {length_guide.get(length, length)} in the {genre} genre based on the following prompt:

{prompt}

Create an engaging title for the story as well."""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
    
    payload = {
        "messages": messages
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                story_text = result.get("result", {}).get("response", "No story generated")
                
                # Try to extract title
                title = "Untitled Story"
                if "Title:" in story_text:
                    parts = story_text.split("Title:")
                    if len(parts) > 1:
                        title_end = parts[1].find("\n")
                        if title_end > 0:
                            title = parts[1][:title_end].strip()
                        else:
                            title = parts[1].strip()
                
                return {
                    "story": story_text,
                    "title": title,
                    "genre": genre,
                    "length": length
                }
            else:
                error = await response.text()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Cloudflare AI Error: {error}"
                )


async def generate_with_openai(prompt: str, genre: str = "general", length: str = "medium") -> dict:
    """Generate story using OpenAI GPT-4o"""
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI API key not configured"
        )
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    length_guide = {
        "short": "a short story (500-1000 words)",
        "medium": "a medium-length story (1000-2000 words)",
        "long": "a long story (2000-5000 words)"
    }
    
    system_msg = f"""{SYSTEM_PROMPT}

Write {length_guide.get(length, length)} in the {genre} genre."""
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Write a story based on: {prompt}"}
        ],
        "temperature": 0.8,
        "max_tokens": 4000
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                story_text = result.get("choices", [{}])[0].get("message", {}).get("content", "No story generated")
                
                title = "Untitled Story"
                if "Title:" in story_text:
                    parts = story_text.split("Title:")
                    if len(parts) > 1:
                        title_end = parts[1].find("\n")
                        if title_end > 0:
                            title = parts[1][:title_end].strip()
                        else:
                            title = parts[1].strip()
                
                return {
                    "story": story_text,
                    "title": title,
                    "genre": genre,
                    "length": length
                }
            else:
                error = await response.text()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"OpenAI API Error: {error}"
                )


@router.post("/generate", response_model=StoryGenerationResponse)
async def generate_story(request: StoryGenerationRequest):
    """Generate story from text prompt"""
    try:
        # Try Cloudflare first, fall back to OpenAI
        if settings.CLOUDFLARE_ACCOUNT_ID and settings.CLOUDFLARE_API_TOKEN:
            result = await generate_with_mistral(
                request.prompt,
                request.genre,
                request.length
            )
        elif settings.OPENAI_API_KEY:
            result = await generate_with_openai(
                request.prompt,
                request.genre,
                request.length
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No AI story generation service configured"
            )
        
        return StoryGenerationResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/genres")
async def get_available_genres():
    """Get available story genres"""
    return {
        "genres": [
            {"id": "general", "name": "General Fiction"},
            {"id": "fantasy", "name": "Fantasy"},
            {"id": "scifi", "name": "Science Fiction"},
            {"id": "romance", "name": "Romance"},
            {"id": "mystery", "name": "Mystery"},
            {"id": "horror", "name": "Horror"},
            {"id": "thriller", "name": "Thriller"},
            {"id": "adventure", "name": "Adventure"},
        ]
    }


@router.get("/models")
async def get_available_models():
    """Get available story generation models"""
    return {
        "models": [
            {"id": "mistral-7b", "name": "Mistral 7B", "provider": "Cloudflare"},
            {"id": "gpt-4o", "name": "GPT-4o", "provider": "OpenAI"},
        ]
    }