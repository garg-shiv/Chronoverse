# Chronoverse Backend API Specification

## Overview

The Chronoverse Backend API provides RESTful endpoints for AI-powered historical character interactions, speech processing, and knowledge retrieval. This document details all available endpoints, request/response formats, and error handling.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API operates without authentication for development purposes. Production deployments should implement proper authentication mechanisms.

## Content Types

- **Request**: `application/x-www-form-urlencoded` (for form data)
- **Response**: `application/json`

## Core Endpoints

### 1. Dialogue Endpoint

**POST** `/api/v1/dialogue`

Main conversation endpoint for interacting with historical characters.

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `character_id` | string | Yes | Character identifier |
| `user_text` | string | No | User's text input |
| `user_audio` | file | No | User's audio input (WAV/MP3) |
| `scene_context` | string | No | Current scene context |
| `session_id` | string | No | Session identifier for memory |

#### Character IDs

- `roman_gladiator` - Marcus Quintus
- `mughal_architect` - Ustad Ahmad Lahauri
- `egyptian_scribe` - Khaemwaset
- `medieval_knight` - Sir Gareth

#### Request Example

```bash
curl -X POST "http://localhost:8000/api/v1/dialogue" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "character_id=roman_gladiator&user_text=Tell me about gladiator training&scene_context=colosseum"
```

#### Response Format

```json
{
  "success": true,
  "character_id": "roman_gladiator",
  "character_name": "Marcus Quintus",
  "response_text": "Ah, you ask about the sacred art of gladiatorial training...",
  "audio_url": "/generated_audio/response_12345.wav",
  "session_id": "session_67890",
  "processing_time": 3.2,
  "knowledge_sources": [
    {
      "fact": "Gladiators trained in specialized schools called ludi",
      "source": "Archaeological evidence from Pompeii",
      "accuracy": "high"
    }
  ],
  "conversation_memory": [
    {
      "user": "Tell me about gladiator training",
      "character": "Ah, you ask about the sacred art..."
    }
  ]
}
```

#### Error Responses

```json
{
  "success": false,
  "error": "Invalid character_id",
  "error_code": "INVALID_CHARACTER",
  "details": "Character 'unknown_character' not found"
}
```

### 2. Characters List

**GET** `/api/v1/characters`

Retrieve list of available historical characters.

#### Response Example

```json
{
  "success": true,
  "characters": [
    {
      "id": "roman_gladiator",
      "name": "Marcus Quintus",
      "title": "Roman Gladiator",
      "period": "1st-2nd Century CE",
      "greeting": "Salve! I am Marcus Quintus, a gladiator of Rome...",
      "personality": "Proud, disciplined, honorable warrior",
      "expertise": ["Gladiatorial combat", "Roman society", "Military training"]
    },
    {
      "id": "mughal_architect",
      "name": "Ustad Ahmad Lahauri",
      "title": "Mughal Architect",
      "period": "17th Century CE",
      "greeting": "Peace be upon you. I am Ustad Ahmad Lahauri...",
      "personality": "Patient, detail-oriented, spiritually minded",
      "expertise": ["Islamic architecture", "Taj Mahal construction", "Geometric design"]
    }
  ]
}
```

## Service Information Endpoints

### 3. Speech-to-Text Service Info

**GET** `/api/v1/stt/info`

Get information about the STT service status and configuration.

#### Response Example

```json
{
  "success": true,
  "service": "OpenAI Whisper",
  "model": "base",
  "model_size": "39M parameters",
  "status": "operational",
  "supported_formats": ["WAV", "MP3", "M4A"],
  "max_audio_duration": 30,
  "processing_time_avg": 1.5
}
```

### 4. Language Model Info

**GET** `/api/v1/llm/info`

Get information about the language model service.

#### Response Example

```json
{
  "success": true,
  "service": "Ollama",
  "model": "llama3.2:3b",
  "model_size": "3 billion parameters",
  "status": "operational",
  "host": "http://127.0.0.1:12345",
  "context_length": 1024,
  "response_time_avg": 2.1
}
```

### 5. Text-to-Speech Service Info

**GET** `/api/v1/tts/info`

Get information about the TTS service configuration.

#### Response Example

```json
{
  "success": true,
  "primary_service": "StreamElements",
  "fallback_service": "VoiceRSS",
  "emergency_service": "espeak",
  "status": "operational",
  "supported_voices": {
    "roman_gladiator": "Marcus",
    "mughal_architect": "Ahmad",
    "egyptian_scribe": "Khaemwaset",
    "medieval_knight": "Gareth"
  },
  "audio_format": "WAV",
  "sample_rate": 22050
}
```

## System Health Endpoints

### 6. Health Check

**GET** `/health`

System health check endpoint.

#### Response Example

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "ollama": "operational",
    "chromadb": "operational",
    "tts": "operational",
    "stt": "operational"
  },
  "uptime": 3600,
  "memory_usage": "1.2GB",
  "cpu_usage": "15%"
}
```

### 7. System Status

**GET** `/api/v1/status`

Detailed system status information.

#### Response Example

```json
{
  "success": true,
  "system_status": {
    "backend": "operational",
    "database": "operational",
    "ai_services": "operational",
    "audio_processing": "operational"
  },
  "performance_metrics": {
    "active_sessions": 5,
    "requests_per_minute": 12,
    "average_response_time": 3.2,
    "error_rate": 0.1
  },
  "resource_usage": {
    "cpu_percentage": 15,
    "memory_usage_mb": 1200,
    "disk_usage_gb": 2.5,
    "network_io_mbps": 5.2
  }
}
```

## Error Handling

### Error Response Format

All error responses follow this format:

```json
{
  "success": false,
  "error": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "details": "Additional error details",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Common Error Codes

| Error Code | Description | HTTP Status |
|------------|-------------|-------------|
| `INVALID_CHARACTER` | Character ID not found | 400 |
| `INVALID_AUDIO_FORMAT` | Unsupported audio format | 400 |
| `AUDIO_TOO_LARGE` | Audio file exceeds size limit | 400 |
| `STT_FAILED` | Speech-to-text processing failed | 500 |
| `LLM_FAILED` | Language model processing failed | 500 |
| `TTS_FAILED` | Text-to-speech generation failed | 500 |
| `KNOWLEDGE_BASE_ERROR` | Knowledge retrieval failed | 500 |
| `SESSION_EXPIRED` | Session has expired | 401 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |
| `SERVICE_UNAVAILABLE` | Service temporarily unavailable | 503 |

### Rate Limiting

- **Default**: 100 requests per minute per IP
- **Burst**: 20 requests per 10 seconds
- **Headers**: Rate limit information included in response headers

## WebSocket Support (Future)

### Real-time Audio Streaming

**WebSocket** `/ws/audio`

For real-time audio streaming (planned for future versions).

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/audio');

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  // Handle real-time audio data
};
```

## SDK Examples

### Python SDK

```python
import requests

class ChronoverseClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def chat(self, character_id, user_text, scene_context=None):
        data = {
            "character_id": character_id,
            "user_text": user_text
        }
        if scene_context:
            data["scene_context"] = scene_context
        
        response = requests.post(f"{self.base_url}/api/v1/dialogue", data=data)
        return response.json()
    
    def get_characters(self):
        response = requests.get(f"{self.base_url}/api/v1/characters")
        return response.json()

# Usage
client = ChronoverseClient()
response = client.chat("roman_gladiator", "Tell me about training")
print(response["response_text"])
```

### JavaScript SDK

```javascript
class ChronoverseClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async chat(characterId, userText, sceneContext = null) {
        const formData = new FormData();
        formData.append('character_id', characterId);
        formData.append('user_text', userText);
        if (sceneContext) {
            formData.append('scene_context', sceneContext);
        }
        
        const response = await fetch(`${this.baseUrl}/api/v1/dialogue`, {
            method: 'POST',
            body: formData
        });
        
        return await response.json();
    }
    
    async getCharacters() {
        const response = await fetch(`${this.baseUrl}/api/v1/characters`);
        return await response.json();
    }
}

// Usage
const client = new ChronoverseClient();
client.chat('roman_gladiator', 'Tell me about training')
    .then(response => console.log(response.response_text));
```

## Testing

### Test Endpoints

Use the interactive API documentation at `http://localhost:8000/docs` for testing endpoints.

### Load Testing

```bash
# Install Apache Bench
ab -n 100 -c 10 -p test_data.json -T application/x-www-form-urlencoded http://localhost:8000/api/v1/dialogue
```

## Versioning

API versioning is handled through URL paths:
- Current version: `/api/v1/`
- Future versions: `/api/v2/`, `/api/v3/`, etc.

## Deprecation Policy

- Deprecated endpoints will be marked with `@deprecated` in documentation
- 6-month notice before removal
- Migration guides provided for breaking changes

---

*For additional API support, contact the development team or check the interactive documentation at `/docs`*
