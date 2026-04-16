# Burme AI - Cloudflare Workers & Pages

This directory contains the Cloudflare Workers configuration for deploying Burme AI as an edge API.

## 📦 Contents

- `index.js` - Cloudflare Worker with AI API endpoints
- `wrangler.toml` - Cloudflare configuration

## 🚀 Quick Deploy

### Prerequisites

1. Cloudflare Account
2. Cloudflare API Token with Workers edit permission

### Deploy with Wrangler

```bash
# Install wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Set secrets
wrangler secret put CLOUDFLARE_API_TOKEN
wrangler secret put CLOUDFLARE_ACCOUNT_ID

# Deploy
wrangler deploy
```

### Deploy with GitHub Actions

1. Add secrets to GitHub:
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`

2. Push to main branch - auto deploys!

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Chat with Llama-3 |
| `/api/image/generate` | POST | Generate images |
| `/api/story/generate` | POST | Generate stories |
| `/api/app/generate` | POST | Generate code |
| `/health` | GET | Health check |

## 📝 Request Examples

### Chat
```bash
curl -X POST https://your-worker.workers.dev/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello!",
    "history": [],
    "model": "llama-3"
  }'
```

### Image Generation
```bash
curl -X POST https://your-worker.workers.dev/api/image/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A sunset over mountains"
  }'
```

## 🌐 Custom Domain

Add custom domain in `wrangler.toml`:

```toml
[[env.production.routes]]
pattern = "api.yourdomain.com"
zone_name = "yourdomain.com"
```

## 📄 License

MIT