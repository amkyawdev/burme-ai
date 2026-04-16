"""
App/Code Generator API - Llama-3 Integration
Handles code generation requests using Cloudflare AI Workers
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
import aiohttp

from app.core.config import settings

router = APIRouter(prefix="/api/app", tags=["App Generator"])


class AppGenerationRequest(BaseModel):
    description: str
    language: Optional[str] = "python"
    framework: Optional[str] = ""
    requirements: Optional[str] = ""


class AppGenerationResponse(BaseModel):
    code: str
    language: str
    files: List[dict]


SYSTEM_PROMPT = """You are an Expert Coder AI assistant. Your task is to generate complete, production-ready code based on the user's description.

Guidelines:
1. Write clean, well-documented code
2. Follow best practices and security guidelines
3. Include proper error handling
4. Use modern language features
5. Provide all necessary files (main, config, requirements, etc.)

When asked to create an application:
- Analyze the requirements thoroughly
- Design a proper structure
- Generate complete, working code
- Include setup instructions in comments"""



async def generate_code_with_llama(description: str, language: str = "python", system_prompt: str = SYSTEM_PROMPT) -> str:
    """Generate code using Cloudflare AI Workers with Llama-3"""
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
    
    user_prompt = f"""Generate a {language} application with the following description:

{description}

Please provide the complete code with all necessary files. Include:
- Main application file
- Requirements/dependencies
- Configuration if needed
- Setup instructions"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    payload = {
        "messages": messages
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("result", {}).get("response", "No code generated")
            else:
                error = await response.text()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Cloudflare AI Error: {error}"
                )


def parse_code_response(response: str, language: str) -> List[dict]:
    """Parse the AI response to extract code files"""
    files = []
    
    # Simple parsing - in production, use more sophisticated parsing
    # Split by file markers if present
    lines = response.split('\n')
    current_file = {"name": f"main.{'py' if language == 'python' else language}", "content": []}
    
    for line in lines:
        if line.startswith("```"):
            continue
        if line.startswith("File:"):
            if current_file["content"]:
                files.append(current_file)
            filename = line.replace("File:", "").strip()
            current_file = {"name": filename, "content": []}
        else:
            current_file["content"].append(line)
    
    if current_file["content"]:
        files.append(current_file)
    
    if not files:
        files = [{"name": f"main.{'py' if language == 'python' else language}", "content": response}]
    
    # Join content
    for file in files:
        if isinstance(file["content"], list):
            file["content"] = "\n".join(file["content"])
    
    return files


@router.post("/generate", response_model=AppGenerationResponse)
async def generate_app(request: AppGenerationRequest):
    """Generate application code from description"""
    try:
        # Add expert coder system prompt
        custom_system = f"""{SYSTEM_PROMPT}

Generate the application in {request.language} language.
{f"Use {request.framework} framework." if request.framework else ""}
{f"Requirements: {request.requirements}" if request.requirements else ""}"""
        
        code = await generate_code_with_llama(
            request.description,
            request.language,
            custom_system
        )
        
        files = parse_code_response(code, request.language)
        
        return AppGenerationResponse(
            code=code,
            language=request.language,
            files=files
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/languages")
async def get_supported_languages():
    """Get supported programming languages"""
    return {
        "languages": [
            {"id": "python", "name": "Python"},
            {"id": "javascript", "name": "JavaScript"},
            {"id": "typescript", "name": "TypeScript"},
            {"id": "html", "name": "HTML"},
            {"id": "css", "name": "CSS"},
            {"id": "java", "name": "Java"},
            {"id": "go", "name": "Go"},
            {"id": "rust", "name": "Rust"},
        ]
    }


@router.get("/models")
async def get_available_models():
    """Get available code generation models"""
    return {
        "models": [
            {"id": "llama-3", "name": "Llama 3", "provider": "Cloudflare"},
            {"id": "codellama-7b", "name": "CodeLlama 7B", "provider": "Cloudflare"},
        ]
    }