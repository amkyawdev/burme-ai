"""
Burme AI Platform - Main Application Entry Point
FastAPI application with Jinja2 templates
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os

from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)


# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "app_name": settings.APP_NAME}
    )


# Chat page
@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Chat with AI"""
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "app_name": settings.APP_NAME}
    )


# Image Generation page
@app.get("/image-gen", response_class=HTMLResponse)
async def image_gen_page(request: Request):
    """Image Generation"""
    return templates.TemplateResponse(
        "image_gen.html",
        {"request": request, "app_name": settings.APP_NAME}
    )


# Video Generation page
@app.get("/video-gen", response_class=HTMLResponse)
async def video_gen_page(request: Request):
    """Video Generation"""
    return templates.TemplateResponse(
        "video_gen.html",
        {"request": request, "app_name": settings.APP_NAME}
    )


# App Generator page
@app.get("/app-gen", response_class=HTMLResponse)
async def app_gen_page(request: Request):
    """App/Code Generator"""
    return templates.TemplateResponse(
        "app_gen.html",
        {"request": request, "app_name": settings.APP_NAME}
    )


# Song Generation page
@app.get("/song-gen", response_class=HTMLResponse)
async def song_gen_page(request: Request):
    """Song Generation"""
    return templates.TemplateResponse(
        "song_gen.html",
        {"request": request, "app_name": settings.APP_NAME}
    )


# Story Generation page
@app.get("/story-gen", response_class=HTMLResponse)
async def story_gen_page(request: Request):
    """Story Generation"""
    return templates.TemplateResponse(
        "story_gen.html",
        {"request": request, "app_name": settings.APP_NAME}
    )


# Docs page
@app.get("/docs", response_class=HTMLResponse)
async def docs_page(request: Request):
    """Documentation page"""
    return templates.TemplateResponse(
        "docs.html",
        {"request": request, "app_name": settings.APP_NAME}
    )


# About page
@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    """About page"""
    return templates.TemplateResponse(
        "about.html",
        {"request": request, "app_name": settings.APP_NAME}
    )


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}
    )


# 404 handler
@app.get("/{path:path}", response_class=HTMLResponse)
async def not_found(request: Request, path: str):
    """404 Not Found page"""
    return templates.TemplateResponse(
        "404.html",
        {"request": request, "app_name": settings.APP_NAME, "path": path},
        status_code=status.HTTP_404_NOT_FOUND
    )


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )