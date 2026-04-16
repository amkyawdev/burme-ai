/**
 * Burme AI Platform - Main JavaScript
 * Handles all frontend interactions and API calls
 */

// API Base URL
const API_BASE = '/api';

// Chat History
let chatHistory = [];

/**
 * Show loading overlay
 */
function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.add('active');
    }
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.remove('active');
    }
}

/**
 * Show error message
 */
function showError(message) {
    alert(message);
}

/**
 * Chat with AI
 */
async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const messagesContainer = document.getElementById('chat-messages');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessage('user', message);
    input.value = '';
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/chat/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                history: chatHistory
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to get response');
        }
        
        const data = await response.json();
        
        // Add assistant message
        addMessage('assistant', data.response);
        
        // Update history
        chatHistory.push({ role: 'user', content: message });
        chatHistory.push({ role: 'assistant', content: data.response });
        
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Add message to chat
 */
function addMessage(role, content) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}`;
    messageDiv.innerHTML = `<p>${escapeHtml(content)}</p>`;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/**
 * Generate Image
 */
async function generateImage() {
    const prompt = document.getElementById('prompt').value.trim();
    const resultContainer = document.getElementById('result-container');
    const resultImage = document.getElementById('result-image');
    
    if (!prompt) {
        showError('Please enter a prompt');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/image/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                num_images: 1
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate image');
        }
        
        const data = await response.json();
        
        if (resultContainer && resultImage) {
            if (data.images && data.images.length > 0) {
                resultImage.src = data.images[0];
                resultContainer.classList.remove('hidden');
            }
        }
        
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Generate Video
 */
async function generateVideo() {
    const prompt = document.getElementById('prompt').value.trim();
    const aspectRatio = document.getElementById('aspect-ratio')?.value || '16:9';
    const resultContainer = document.getElementById('result-container');
    const resultVideo = document.getElementById('result-video');
    
    if (!prompt) {
        showError('Please enter a prompt');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/video/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                aspect_ratio: aspectRatio
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate video');
        }
        
        const data = await response.json();
        
        if (resultContainer && resultVideo) {
            if (data.video_url) {
                resultVideo.src = data.video_url;
                resultContainer.classList.remove('hidden');
            }
        }
        
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Generate App/Code
 */
async function generateApp() {
    const description = document.getElementById('description').value.trim();
    const language = document.getElementById('language')?.value || 'python';
    const resultContainer = document.getElementById('result-container');
    const resultCode = document.getElementById('result-code');
    
    if (!description) {
        showError('Please enter a description');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/app/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                description: description,
                language: language
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate code');
        }
        
        const data = await response.json();
        
        if (resultContainer && resultCode) {
            resultCode.textContent = data.code;
            resultContainer.classList.remove('hidden');
        }
        
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Generate Song
 */
async function generateSong() {
    const prompt = document.getElementById('prompt').value.trim();
    const duration = parseInt(document.getElementById('duration')?.value || '30');
    const resultContainer = document.getElementById('result-container');
    const resultAudio = document.getElementById('result-audio');
    
    if (!prompt) {
        showError('Please enter a prompt');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/audio/song`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                duration: duration
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate song');
        }
        
        const data = await response.json();
        
        if (resultContainer && resultAudio) {
            if (data.song_url) {
                resultAudio.src = data.song_url;
                resultContainer.classList.remove('hidden');
            }
        }
        
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Generate Story
 */
async function generateStory() {
    const prompt = document.getElementById('prompt').value.trim();
    const genre = document.getElementById('genre')?.value || 'general';
    const length = document.getElementById('length')?.value || 'medium';
    const resultContainer = document.getElementById('result-container');
    const resultStory = document.getElementById('result-story');
    
    if (!prompt) {
        showError('Please enter a prompt');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/story/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                genre: genre,
                length: length
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate story');
        }
        
        const data = await response.json();
        
        if (resultContainer && resultStory) {
            resultStory.innerHTML = `<h3>${escapeHtml(data.title)}</h3><p>${escapeHtml(data.story)}</p>`;
            resultContainer.classList.remove('hidden');
        }
        
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Convert Text to Speech
 */
async function convertToSpeech() {
    const text = document.getElementById('text').value.trim();
    const voice = document.getElementById('voice')?.value || 'alloy';
    const resultContainer = document.getElementById('result-container');
    const resultAudio = document.getElementById('result-audio');
    
    if (!text) {
        showError('Please enter text');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/audio/tts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                voice: voice
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to convert text to speech');
        }
        
        const data = await response.json();
        
        if (resultContainer && resultAudio) {
            if (data.audio_url) {
                resultAudio.src = data.audio_url;
                resultContainer.classList.remove('hidden');
            }
        }
        
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Initialize event listeners
 */
document.addEventListener('DOMContentLoaded', function() {
    // Chat input enter key
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }
    
    // Auto-resize textarea
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
});