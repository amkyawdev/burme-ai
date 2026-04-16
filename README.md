# 🤖 Burme AI Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00B4D8?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

AI-Powered Platform for Chat, Image Generation, Video Generation, App Generation, Song Generation, and Story Generation.

[简体中文](./README.zh.md) · [English](./README.md) · [Burmese](./README.mm.md)

</div>

---

## ✨ Features

| Feature | Description | AI Model |
|---------|-------------|----------|
| 🤖 **AI Chat** | Chat with AI assistant | Llama-3 (Cloudflare) |
| 🖼️ **Image Generation** | Generate images from text | Stable Diffusion / DALL-E |
| 🎬 **Video Generation** | Create videos from text | PixVerse API |
| 📱 **App Generator** | Text to Code | Llama-3 (Expert Coder) |
| 🎵 **Song Generation** | Create music with AI | AudioCraft (MusicGen) |
| 📖 **Story Generation** | Write creative stories | Mistral-7b / GPT-4o |

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** HTML/CSS/JavaScript with Jinja2 Templates
- **Database:** Ready for integration
- **AI Models:** Cloudflare AI Workers, OpenAI, Hugging Face

---

## 📂 Project Structure

```
burme-ai/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application Entry Point
│   ├── core/                   # Configurations & Security
│   │   ├── config.py           # Environment Variables
│   │   └── security.py         # Security Utilities
│   ├── api/                    # AI Model Endpoints
│   │   ├── chatbot.py          # Llama-3 Chat
│   │   ├── image_gen.py        # Image Generation
│   │   ├── video_gen.py        # Video Generation
│   │   ├── audio_gen.py        # Audio/TTS Generation
│   │   ├── app_gen.py          # Code Generator
│   │   └── story_gen.py        # Story Generator
│   ├── services/               # Third-party APIs
│   │   ├── cloudflare_ai.py   # Cloudflare AI
│   │   └── pixverse_api.py    # PixVerse Video
│   ├── static/                 # Assets
│   │   ├── css/style.css      # Glassmorphism Theme
│   │   └── js/main.js         # Frontend JS
│   └── templates/              # HTML Templates
│       ├── base.html
│       ├── index.html
│       ├── chat.html
│       ├── image_gen.html
│       ├── video_gen.html
│       ├── app_gen.html
│       ├── song_gen.html
│       ├── story_gen.html
│       ├── docs.html
│       ├── about.html
│       └── 404.html
├── requirements.txt            # Python Dependencies
├── .env                       # Environment Variables
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- pip or uv

### Installation

```bash
# Clone the repository
git clone https://github.com/amkyawdev/burme-ai.git
cd burme-ai

# Install dependencies
pip install -r requirements.txt

# OR use uv
uv venv && uv sync
```

### Configuration

Create a `.env` file:

```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Cloudflare AI (Llama-3, Mistral-7b, Stable Diffusion)
CLOUDFLARE_ACCOUNT_ID=your_account_id
CLOUDFLARE_API_TOKEN=your_api_token

# OpenAI (GPT-4o, DALL-E, TTS)
OPENAI_API_KEY=your_openai_key

# PixVerse API (Video Generation)
PIXVERSE_API_KEY=your_pixverse_key
```

### Run the Server

```bash
# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Open Browser

```
http://localhost:8000
```

---

## 🎨 Design Theme

### Color Palette

| Color | Hex Code | Usage |
|-------|----------|-------|
| Primary Blue | #00B4D8 | Buttons, Links, Icons |
| Background | #F8FBFF | Page Background |
| Card BG | rgba(255,255,255,0.7) | Glassmorphism Cards |

### Glassmorphism Style

```css
.glass-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}
```

---

## 📖 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/` | Chat with AI |
| POST | `/api/image/generate` | Generate Images |
| POST | `/api/video/generate` | Generate Videos |
| POST | `/api/app/generate` | Generate Code |
| POST | `/api/audio/song` | Generate Songs |
| POST | `/api/audio/tts` | Text to Speech |
| POST | `/api/story/generate` | Generate Stories |

---

## 🔧 Development

### Run Tests

```bash
pytest
```

### Code Format

```bash
ruff check .
ruff format .
```

---
## Cloudflare Deployment

### Workers (Serverless API)

Deploy AI APIs to Cloudflare Workers:

```bash
npm install -g wrangler
wrangler login
wrangler secret put CLOUDFLARE_API_TOKEN
wrangler secret put CLOUDFLARE_ACCOUNT_ID
wrangler deploy
```

See `/workers/README.md` for details.

### Pages
Deploy frontend to Cloudflare Pages.

### GitHub Actions
Add secrets: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID

## 📄 License

MIT License - feel free to use this project for any purpose.

---

## 👨‍💻 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

<div align="center">

Made with ❤️ by [Burme AI](https://github.com/amkyawdev)

</div>