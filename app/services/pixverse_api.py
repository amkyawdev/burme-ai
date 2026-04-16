"""
PixVerse API Service
Handles PixVerse video generation API interactions
"""

import aiohttp
import asyncio
from typing import Optional, Dict, Any

from app.core.config import settings


class PixVerseService:
    """Service for interacting with PixVerse API"""
    
    def __init__(self):
        self.api_key = settings.PIXVERSE_API_KEY
        self.base_url = "https://api.pixverse.ai/api/v1"
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def text_to_video(
        self,
        prompt: str,
        aspect_ratio: str = "16:9",
        negative_prompt: str = "",
        wait_for_completion: bool = True,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """Generate video from text prompt"""
        if not self.api_key:
            raise ValueError("PixVerse API key not configured")
        
        url = f"{self.base_url}/t2v"
        
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
        }
        
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt
        
        async with aiohttp.ClientSession() as session:
            # Submit generation request
            async with session.post(url, json=payload, headers=self._get_headers()) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"PixVerse API Error: {error}")
                
                result = await response.json()
                task_id = result.get("data", {}).get("task_id", "")
                
                if not task_id:
                    raise Exception("Failed to get task ID from PixVerse")
            
            if not wait_for_completion:
                return {
                    "task_id": task_id,
                    "status": "processing"
                }
            
            # Poll for results
            return await self._wait_for_completion(session, task_id, timeout)
    
    async def _wait_for_completion(self, session: aiohttp.ClientSession, task_id: str, timeout: int) -> Dict[str, Any]:
        """Wait for video generation to complete"""
        status_url = f"{self.base_url}/t2v/{task_id}/status"
        
        start_time = asyncio.get_event_loop().time()
        
        while True:
            async with session.get(status_url, headers=self._get_headers()) as response:
                if response.status == 200:
                    result = await response.json()
                    data = result.get("data", {})
                    status = data.get("status", "")
                    
                    if status == "completed":
                        return {
                            "task_id": task_id,
                            "status": "completed",
                            "video_url": data.get("video_url", "")
                        }
                    elif status == "failed":
                        raise Exception("Video generation failed")
                    
                    # Check timeout
                    if asyncio.get_event_loop().time() - start_time > timeout:
                        raise Exception("Video generation timed out")
                    
                    await asyncio.sleep(2)
                else:
                    await asyncio.sleep(2)
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of a video generation task"""
        url = f"{self.base_url}/t2v/{task_id}/status"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._get_headers()) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"Failed to get task status: {await response.text()}")


# Singleton instance
pixverse_service = PixVerseService()