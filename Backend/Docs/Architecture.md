# Chronoverse Architecture Documentation

## System Overview

Chronoverse is built on a microservices-inspired architecture with integrated AI components for natural language processing, knowledge retrieval, and voice synthesis. The system consists of a sophisticated AI backend that communicates with an Unreal Engine 5 client through RESTful APIs.

## High-Level Architecture

```
┌─────────────────┐    HTTP/WebSocket    ┌─────────────────┐
│   UE5 Client    │ ←──────────────────→ │  AI Backend     │
│                 │                      │                 │
│ • 3D Rendering  │                      │ • FastAPI       │
│ • Voice Input   │                      │ • AI Services   │
│ • UI/UX         │                      │ • Knowledge DB  │
│ • Audio Output  │                      │ • Session Mgmt  │
└─────────────────┘                      └─────────────────┘
         │                                        │
         │                                        │
         ▼                                        ▼
┌─────────────────┐                      ┌─────────────────┐
│   User Input    │                      │  External APIs  │
│                 │                      │                 │
│ • Voice         │                      │ • TTS Services  │
│ • Text          │                      │ • STT Services  │
│ • Movement      │                      │ • LLM Services  │
└─────────────────┘                      └─────────────────┘
```

## Core Components

### 1. Speech-to-Text Service (`core/stt.py`)
- **Technology**: OpenAI Whisper
- **Model**: `base` (39M parameters, CPU optimized)
- **Processing**: Real-time audio transcription
- **Performance**: ~1-2 seconds for 10-second audio clips
- **Supported Formats**: WAV, MP3, M4A, FLAC
- **Max Duration**: 30 seconds per audio clip

### 2. Knowledge Retrieval System (`core/rag.py`)
- **Technology**: ChromaDB + Sentence Transformers
- **Embedding Model**: `all-MiniLM-L6-v2` (23M parameters)
- **Storage**: Persistent vector database with SQLite backend
- **Retrieval**: Top-3 relevant facts per query with similarity scoring
- **Indexing**: Automatic embedding generation for new facts
- **Performance**: ~100ms for knowledge retrieval

### 3. Language Model Service (`core/llm.py`)
- **Technology**: Ollama + llama3.2:3b
- **Model Size**: 3 billion parameters
- **Optimization**: CPU inference with Intel graphics acceleration
- **Response Generation**: Character-specific dialogue with memory
- **Context Length**: 1024 tokens
- **Temperature**: 0.7 for creative responses
- **Performance**: ~2-3 seconds for response generation

### 4. Text-to-Speech Service (`core/tts.py`)
- **Architecture**: Multi-provider fallback system
- **Primary**: StreamElements API (high quality, character voices)
- **Secondary**: VoiceRSS API (reliable, multiple languages)
- **Emergency**: Local espeak (offline capability)
- **Character Voices**: Unique voice profiles per character
- **Audio Format**: WAV, 22050Hz sample rate
- **Performance**: ~1-2 seconds for audio generation

### 5. Session Management (`core/session_manager.py`)
- **Memory**: In-memory session storage
- **Persistence**: 30-minute session timeout
- **Context**: Last 3 exchanges per conversation
- **Cleanup**: Automatic expired session removal

## Data Flow Architecture

### Complete Request Flow
```
[User Voice Input] → [UE5 Audio Capture] → [HTTP Request]
                                                        ↓
[Audio Processing] ← [TTS Response] ← [LLM Generation] ← [RAG Retrieval] ← [STT Processing]
                                                        ↓
[User Audio Response] ← [UE5 Audio Playback] ← [Audio File Generation]
```

### Intelligent Query Routing
```
User Query → Query Classification → Decision Tree
                                    ↓
                            [Conversational Query] → [LLM Only] → [Response]
                                    ↓
                            [Historical Query] → [RAG + LLM] → [Response]
                                    ↓
                            [Mixed Query] → [RAG + LLM + Context] → [Response]
```

### Multi-Service TTS Architecture
```
Text Input → Primary TTS (StreamElements) → Success?
                                    ↓ No
                            Fallback TTS (VoiceRSS) → Success?
                                    ↓ No
                            Emergency TTS (espeak) → Audio Output
```

## Performance Characteristics

### Response Times
- **Conversational**: 2-3 seconds (LLM only)
- **Educational**: 3-5 seconds (RAG + LLM)
- **Voice Processing**: +1-2 seconds (STT + TTS)
- **Total End-to-End**: 4-7 seconds

### Resource Usage
- **CPU**: Optimized for Intel integrated graphics
- **Memory**: ~2GB RAM for full stack
- **Storage**: ~500MB for models + knowledge base
- **Network**: Minimal (TTS APIs only)

### Scalability Metrics
- **Concurrent Users**: 10+ simultaneous conversations
- **Throughput**: 100+ requests per minute
- **Session Capacity**: 1000+ active sessions
- **Knowledge Base**: 1000+ facts with sub-second retrieval

## Security Architecture

### API Security
- **Input Validation**: Pydantic models for all requests
- **Rate Limiting**: Per-IP and per-session limits
- **Audio Sanitization**: File type and size validation
- **CORS Configuration**: Controlled cross-origin access

### Data Privacy
- **Session Data**: In-memory only, automatic cleanup
- **Audio Files**: Temporary storage with cleanup
- **Knowledge Base**: Read-only historical facts
- **No User PII**: No personal information stored

## Deployment Architecture

### Development Environment
```
[Local Machine]
├── Ollama Server (Port 12345)
├── FastAPI Backend (Port 8000)
├── ChromaDB (Local File Storage)
├── Audio Files (Local Directory)
└── UE5 Client (Local Development)
```

### Production Environment
```
[Load Balancer]
       ↓
[FastAPI Instances] × N
       ↓
[Ollama Server]
       ↓
[ChromaDB (Local Storage)]
       ↓
[Audio Files (Local Storage)]
```

## Technology Stack

### Backend Framework
- **FastAPI**: Async Python web framework with automatic OpenAPI generation
- **Uvicorn**: ASGI server with auto-reload and worker processes
- **Pydantic**: Data validation and serialization with type hints

### AI/ML Stack
- **OpenAI Whisper**: Speech recognition for audio processing
- **ChromaDB**: Vector database for semantic search
- **Sentence Transformers**: Text embedding generation
- **Ollama**: Local LLM inference server

### Infrastructure
- **Ollama**: Local LLM inference server with model management
- **ChromaDB**: Vector database with SQLite backend
- **File System**: Local storage for audio files and knowledge base

### UE5 Integration
- **HTTP Client**: RESTful API communication
- **JSON Serialization**: Request/response data format
- **Audio Processing**: Real-time audio capture and playback
- **VoiceComm Plugin**: Custom UE5 plugin for voice integration

## Error Handling Strategy

### Graceful Degradation
1. **TTS Failure**: Return text-only response with audio generation retry
2. **STT Failure**: Prompt for text input with confidence indicators
3. **RAG Failure**: Use LLM-only generation with fallback knowledge
4. **LLM Failure**: Return predefined character greeting with error logging
5. **Network Failure**: Offline mode with cached responses

### Recovery Mechanisms
- **Service Restart**: Automatic service recovery with health checks
- **Circuit Breaker**: Prevent cascade failures with timeout handling
- **Fallback Responses**: Maintain user experience during outages
- **Health Checks**: Proactive service monitoring and alerting

## Integration Patterns

### UE5 Client Integration
```cpp
// VoiceCommComponent.h
class UVoiceCommComponent : public UActorComponent
{
    GENERATED_BODY()
    
public:
    UFUNCTION(BlueprintCallable)
    void SendVoiceToBackend(const FString& AudioData);
    
    UFUNCTION(BlueprintCallable)
    void SendTextToBackend(const FString& Text);
    
    UFUNCTION(BlueprintCallable)
    void PlayAudioResponse(const FString& AudioUrl);
    
private:
    void OnBackendResponse(const FBackendResponse& Response);
    void HandleError(const FString& ErrorMessage);
};
```

### API Integration Example
```python
# Backend API endpoint
@app.post("/api/v1/dialogue")
async def dialogue_endpoint(
    character_id: str = Form(...),
    user_text: Optional[str] = Form(None),
    user_audio: Optional[UploadFile] = File(None),
    scene_context: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None)
):
    # Process request and return response
    return {
        "success": True,
        "character_id": character_id,
        "response_text": response_text,
        "audio_url": audio_url,
        "session_id": session_id
    }
```

---

*This architecture provides a robust foundation for the Chronoverse platform, enabling immersive historical education through AI and 3D technology.*
