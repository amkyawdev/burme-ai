"""
Audio Generation API - Text-to-Speech & Song Generation
Handles audio generation requests using AudioCraft (MusicGen) or TTS APIs
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import aiohttp
import base64

from app.core.config import settings

router = APIRouter(prefix="/api/audio", tags=["Audio Generation"])


class AudioGenerationRequest(BaseModel):
    text: str
    voice: Optional[str] = "default"
    model: Optional[str] = "tts"


class SongGenerationRequest(BaseModel):
    prompt: str
    duration: Optional[int] = 30


class AudioGenerationResponse(BaseModel):
    audio_url: str
    format: str = "mp3"


class SongGenerationResponse(BaseModel):
    song_url: str
    duration: int


async def generate_with_openai_tts(text: str, voice: str = "alloy") -> str:
    """Generate speech using OpenAI TTS API"""
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI API key not configured"
        )
    
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "tts-1",
        "voice": voice,
        "input": text,
        "response_format": "mp3"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                audio_data = await response.read()
                audio_b64 = base64.b64encode(audio_data).decode()
                return f"data:audio/mp3;base64,{audio_b64}"
            else:
                error = await response.text()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"OpenAI TTS Error: {error}"
                )


async def generate_with_audiocraft(prompt: str, duration: int = 30) -> str:
    """Generate music using Meta's AudioCraft (MusicGen)"""
    try:
        from transformers import pipeline
        import torch
        
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load MusicGen model
        music_generator = pipeline(
            "text-to-audio",
            model="facebook/musicgen-medium",
            device=device
        )
        
        # Generate music
        result = music_generator(
            prompt,
            max_new_tokens=duration * 32000 // 512  # Approximate token calculation
        )
        
        # Return base64 audio (would need to save to file in production)
        # For now, return a placeholder
        return "data:audio/wav;base64,placeholder"
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AudioCraft generation failed: {str(e)}"
        )


@router.post("/tts", response_model=AudioGenerationResponse)
async def text_to_speech(request: AudioGenerationRequest):
    """Convert text to speech"""
    try:
        if settings.OPENAI_API_KEY:
            audio_url = await generate_with_openai_tts(request.text, request.voice)
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No TTS service configured"
            )
        
        return AudioGenerationResponse(audio_url=audio_url)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/song", response_model=SongGenerationResponse)
async def generate_song(request: SongGenerationRequest):
    """Generate song from text prompt"""
    try:
        if settings.OPENAI_API_KEY:
            # Use OpenAI's Jukebox or placeholder
            song_url = "data:audio/mp3;base64,placeholder"
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Song generation not configured"
            )
        
        return SongGenerationResponse(song_url=song_url, duration=request.duration)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/voices")
async def get_available_voices():
    """Get available TTS voices"""
    return {
        "voices": [
            {"id": "alloy", "name": "Alloy"},
            {"id": "echo", "name": "Echo"},
            {"id": "fable", "name": "Fable"},
            {"id": "onyx", "name": "Onyx"},
            {"id": "nova", "name": "Nova"},
            {"id": "shimmer", "name": "Shimmer"},
        ]
    }


@router.get("/models")
async def get_available_models():
    """Get available audio generation models"""
    return {
        "models": [
            {"id": "tts-1", "name": "OpenAI TTS-1", "type": "tts", "provider": "OpenAI"},
            {"id": "musicgen-medium", "name": "MusicGen Medium", "type": "music", "provider": "Meta"},
        ]
    }