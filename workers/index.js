/**
 * Burme AI Cloudflare Worker
 * Handles AI API requests: Chat, Image Generation, Story Generation
 */

// API Configuration - Set these in Cloudflare Dashboard or wrangler secret
const CLOUDFLARE_ACCOUNT_ID = 'your_account_id';
const CLOUDFLARE_API_TOKEN = 'your_api_token';

const AI_MODELS = {
  'llama-3': '@cf/meta/llama-3-8b-chat',
  'llama-3.1': '@cf/meta/llama-3.1-70b-instruct',
  'mistral-7b': '@cf/meta/mistral-7b-instruct-v0.1',
  'stable-diffusion': '@cf/stabilityai/stable-diffusion-xl-base-1.0',
};

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

/**
 * Handle CORS preflight requests
 */
async function handleCors(request) {
  return new Response(null, { headers: CORS_HEADERS });
}

/**
 * Call Cloudflare AI API
 */
async function callAI(modelId, messages, options = {}) {
  const model = AI_MODELS[modelId] || modelId;
  const url = `https://api.cloudflare.com/client/v4/accounts/${CLOUDFLARE_ACCOUNT_ID}/ai/run/${model}`;
  
  const headers = {
    'Authorization': `Bearer ${CLOUDFLARE_API_TOKEN}`,
    'Content-Type': 'application/json',
  };
  
  const payload = {
    messages,
    ...options,
  };
  
  const response = await fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload),
  });
  
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`AI API Error: ${error}`);
  }
  
  return await response.json();
}

/**
 * Chat API Handler
 */
async function handleChat(request) {
  try {
    const body = await request.json();
    const { message, history = [], model = 'llama-3', system_prompt } = body;
    
    const messages = [];
    
    if (system_prompt) {
      messages.push({ role: 'system', content: system_prompt });
    }
    
    // Add conversation history
    for (const msg of history) {
      messages.push({ role: msg.role, content: msg.content });
    }
    
    // Add current message
    messages.push({ role: 'user', content: message });
    
    const result = await callAI(model, messages);
    
    return new Response(JSON.stringify({
      response: result.result?.response || 'No response',
      model: model,
    }), {
      headers: {
        ...CORS_HEADERS,
        'Content-Type': 'application/json',
      },
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        ...CORS_HEADERS,
        'Content-Type': 'application/json',
      },
    });
  }
}

/**
 * Image Generation Handler
 */
async function handleImageGen(request) {
  try {
    const body = await request.json();
    const { prompt, model = 'stable-diffusion' } = body;
    
    const result = await callAI(model, [
      { role: 'user', content: prompt }
    ]);
    
    return new Response(JSON.stringify({
      images: [result.result?.image || ''],
      model: model,
    }), {
      headers: {
        ...CORS_HEADERS,
        'Content-Type': 'application/json',
      },
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        ...CORS_HEADERS,
        'Content-Type': 'application/json',
      },
    });
  }
}

/**
 * Story Generation Handler
 */
async function handleStoryGen(request) {
  try {
    const body = await request.json();
    const { prompt, genre = 'general', length = 'medium', model = 'mistral-7b' } = body;
    
    const systemPrompt = `You are a Creative Story Writer. Write ${length} stories in ${genre} genre.`;
    
    const messages = [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: prompt }
    ];
    
    const result = await callAI(model, messages);
    
    return new Response(JSON.stringify({
      story: result.result?.response || 'No story generated',
      title: 'Generated Story',
      genre: genre,
      length: length,
    }), {
      headers: {
        ...CORS_HEADERS,
        'Content-Type': 'application/json',
      },
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        ...CORS_HEADERS,
        'Content-Type': 'application/json',
      },
    });
  }
}

/**
 * App/Code Generation Handler
 */
async function handleAppGen(request) {
  try {
    const body = await request.json();
    const { description, language = 'python' } = body;
    
    const systemPrompt = `You are an Expert Coder. Generate complete, production-ready code in ${language}.`;
    
    const messages = [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: description }
    ];
    
    const result = await callAI('llama-3', messages);
    
    return new Response(JSON.stringify({
      code: result.result?.response || 'No code generated',
      language: language,
      files: [{ name: `main.${language === 'javascript' ? 'js' : language}`, content: result.result?.response || '' }],
    }), {
      headers: {
        ...CORS_HEADERS,
        'Content-Type': 'application/json',
      },
    });
    
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: {
        ...CORS_HEADERS,
        'Content-Type': 'application/json',
      },
    });
  }
}

/**
 * Main Request Handler
 */
async function handleRequest(request) {
  // Handle CORS preflight
  if (request.method === 'OPTIONS') {
    return handleCors(request);
  }
  
  const url = new URL(request.url);
  const path = url.pathname;
  
  // API Routes
  if (path === '/api/chat' && request.method === 'POST') {
    return handleChat(request);
  }
  
  if (path === '/api/image/generate' && request.method === 'POST') {
    return handleImageGen(request);
  }
  
  if (path === '/api/story/generate' && request.method === 'POST') {
    return handleStoryGen(request);
  }
  
  if (path === '/api/app/generate' && request.method === 'POST') {
    return handleAppGen(request);
  }
  
  // Health check
  if (path === '/health') {
    return new Response(JSON.stringify({ status: 'healthy', worker: 'burme-ai' }), {
      headers: {
        ...CORS_HEADERS,
        'Content-Type': 'application/json',
      },
    });
  }
  
  // Default response
  return new Response(JSON.stringify({
    message: 'Burme AI Worker',
    endpoints: [
      'POST /api/chat',
      'POST /api/image/generate',
      'POST /api/story/generate',
      'POST /api/app/generate',
      'GET /health',
    ],
  }), {
    headers: {
      ...CORS_HEADERS,
      'Content-Type': 'application/json',
    },
  });
}

// Export the fetch handler for Cloudflare Workers
export default {
  fetch(request, env, ctx) {
    return handleRequest(request);
  },
};