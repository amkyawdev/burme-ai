"""
Cloudflare AI Service
Handles all Cloudflare AI Workers API interactions
"""

import aiohttp
from typing import Optional, List, Dict, Any

from app.core.config import settings


class CloudflareAIService:
    """Service for interacting with Cloudflare AI Workers"""
    
    def __init__(self):
        self.account_id = settings.CLOUDFLARE_ACCOUNT_ID
        self.api_token = settings.CLOUDFLARE_API_TOKEN
        self.base_url = "https://api.cloudflare.com/client/v4/accounts"
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    async def run_model(
        self,
        model_id: str,
        messages: List[Dict[str, str]],
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Run an AI model with the given messages"""
        if not self.account_id or not self.api_token:
            raise ValueError("Cloudflare credentials not configured")
        
        url = f"{self.base_url}/{self.account_id}/ai/run/{model_id}"
        
        payload = {"messages": messages}
        if options:
            payload.update(options)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=self._get_headers()) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error = await response.text()
                    raise Exception(f"Cloudflare AI Error: {error}")
    
    async def chat(
        self,
        prompt: str,
        model: str = "@cf/meta/llama-3-8b-chat",
        system_prompt: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Chat with an AI model"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if history:
            messages.extend(history)
        
        messages.append({"role": "user", "content": prompt})
        
        result = await self.run_model(model, messages)
        return result.get("result", {}).get("response", "")
    
    async def generate_image(self, prompt: str, model: str = "@cf/stabilityai/stable-diffusion-xl-base-1.0") -> str:
        """Generate an image"""
        result = await self.run_model(model, [{"role": "user", "content": prompt}])
        return result.get("result", {}).get("image", "")
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """List available AI models"""
        url = f"{self.base_url}/{self.account_id}/ai/models"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self._get_headers()) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("result", {}).get("models", [])
                else:
                    return []


# Singleton instance
cloudflare_ai = CloudflareAIService()