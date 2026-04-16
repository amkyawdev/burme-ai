// Burme AI - Cloudflare Worker
// API endpoints for AI features

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Health check
    if (path === '/health') {
      return new Response(JSON.stringify({ status: 'ok', service: 'burme-ai' }), {
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      });
    }

    // API Routes
    if (path === '/api/chat' && request.method === 'POST') {
      try {
        const { message, history } = await request.json();
        
        // Using Cloudflare AI (Llama-3)
        const response = await fetch(
          `https://api.cloudflare.com/client/v4/accounts/${env.CLOUDFLARE_ACCOUNT_ID}/ai/run/@cf/meta/llama-3-8b-instruct`,
          {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${env.CLOUDFLARE_API_TOKEN}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              messages: [...history, { role: 'user', content: message }],
            }),
          }
        );
        
        const data = await response.json();
        return new Response(JSON.stringify({ response: data.result.response }), {
          headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
      } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), {
          status: 500,
          headers: { 'Content-Type': 'application/json', ...corsHeaders },
        });
      }
    }

    // Image generation placeholder
    if (path === '/api/image/generate' && request.method === 'POST') {
      return new Response(JSON.stringify({ 
        message: 'Use external API (Replicate/Cloudflare Images)' 
      }), {
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      });
    }

    // Story generation
    if (path === '/api/story/generate' && request.method === 'POST') {
      return new Response(JSON.stringify({ 
        message: 'Use external API (OpenAI/Cloudflare)' 
      }), {
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      });
    }

    // App/Code generation
    if (path === '/api/app/generate' && request.method === 'POST') {
      return new Response(JSON.stringify({ 
        message: 'Use Cloudflare AI for code generation' 
      }), {
        headers: { 'Content-Type': 'application/json', ...corsHeaders },
      });
    }

    // Default: 404
    return new Response(JSON.stringify({ error: 'Not found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json', ...corsHeaders },
    });
  },
};