# Burme AI Platform

AI-Powered Platform for Chat, Image Generation, Video Generation, App Generation, Song Generation, and Story Generation.

## Features

- 🤖 **Chat with AI** - Llama-3 powered chatbot
- 🖼️ **Image Generation** - Stable Diffusion / DALL-E
- 🎬 **Video Generation** - PixVerse API integration
- 📱 **App Generator** - Text to Code with Llama-3
- 🎵 **Song Generation** - AudioCraft (MusicGen)
- 📖 **Story Generation** - GPT-4o / Mistral-7b

## Tech Stack

- **Backend:** FastAPI
- **Frontend:** HTML/CSS/JS with Jinja2 Templates
- **AI Models:** Cloudflare AI Workers, OpenAI, Hugging Face

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# Open browser
http://localhost:8000
```

## Environment Variables

Create a `.env` file with the following:

```env
# Cloudflare AI
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_API_TOKEN=your_api_token

# OpenAI
OPENAI_API_KEY=your_openai_key

# PixVerse
PIXVERSE_API_KEY=your_pixverse_key
```

## License

MIT