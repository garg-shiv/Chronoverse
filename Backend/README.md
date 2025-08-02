# Chronoverse Backend - AI-Powered Historical Education Platform 🏛️

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)]()
[![Voice Enabled](https://img.shields.io/badge/Voice-Enabled-orange.svg)]()
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-green.svg)](https://chromadb.ai)
[![Ollama](https://img.shields.io/badge/Ollama-LLM%20Server-blue.svg)](https://ollama.ai)

A sophisticated AI-powered backend that enables immersive conversations with historically accurate characters through advanced speech recognition, knowledge retrieval, and voice synthesis technologies. This backend serves as the core AI engine for the Chronoverse platform, providing RESTful APIs for the Unreal Engine 5 client.

## 🌟 **Features**

### **🎭 Historical Characters**
- **Marcus Quintus** - Roman Gladiator (1st-2nd Century CE)
- **Ustad Ahmad Lahauri** - Mughal Architect (17th Century CE) 
- **Khaemwaset** - Egyptian Royal Scribe (New Kingdom, 19th Dynasty)
- **Sir Gareth** - Medieval Knight (14th Century CE)

### **🤖 AI Technologies**
- **Speech-to-Text**: OpenAI Whisper for voice input processing
- **Knowledge Retrieval**: ChromaDB with RAG for historically accurate responses
- **Language Model**: Ollama with llama3.2:3b for intelligent dialogue generation
- **Conversation Memory**: Session-based context tracking for natural conversations
- **Text-to-Speech**: Multi-service TTS with character-specific voices

### **🎓 Educational Excellence**
- **University-level historical content** with proper source attribution
- **15+ professionally researched facts** per character
- **Contextual conversations** that reference previous exchanges
- **Multi-modal learning** through voice and text interaction

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.13+
- Ollama with llama3.2:3b model
- Windows/Linux/macOS
- 4GB+ RAM (8GB recommended)
- 2GB+ free disk space

### **Installation**

1. **Clone and setup environment:**
```bash
git clone <your-repo-url>
cd Chronoverse/Backend
python -m venv chronoverse_env
source chronoverse_env/bin/activate  # Linux/Mac
chronoverse_env\Scripts\Activate.ps1  # Windows
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup Ollama:**
```bash
# Set custom port to avoid conflicts
export OLLAMA_HOST=http://127.0.0.1:12345  # Linux/Mac
$env:OLLAMA_HOST = "http://127.0.0.1:12345"  # Windows

ollama serve
ollama pull llama3.2:3b
```

4. **Initialize knowledge base:**
```bash
python -m app.utils.knowledge_seeder
```

5. **Start the server:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

6. **Test the API:**
Visit `http://localhost:8000/docs` for interactive API documentation.

## 📡 **API Endpoints**

### **Core Dialogue**
- `POST /api/v1/dialogue` - Main conversation endpoint with voice/text input
- `GET /api/v1/characters` - List available historical characters

### **Service Information**
- `GET /api/v1/stt/info` - Speech-to-Text service status
- `GET /api/v1/llm/info` - Language model information  
- `GET /api/v1/tts/info` - Text-to-Speech service details
- `GET /health` - System health check

### **Example API Usage**

```python
import requests

# Text conversation
response = requests.post("http://localhost:8000/api/v1/dialogue", data={
    "character_id": "roman_gladiator",
    "user_text": "Tell me about gladiator training techniques",
    "scene_context": "gladiator_training_ground"
})

result = response.json()
print(f"Marcus: {result['response_text']}")
print(f"Audio: {result['audio_url']}")  # Character voice response
```

text

## 🏗️ **Architecture**

### **Request Flow**
```
User Input (Voice/Text) → STT → Query Classification → RAG Retrieval → LLM Generation → TTS → Response
```

### **Intelligent Query Routing**
- **Conversational queries** → LLM-only (2-3 seconds)
- **Historical queries** → RAG + LLM (3-5 seconds)

### **Multi-Service TTS Architecture**
Primary: StreamElements TTS → Fallback: VoiceRSS → Emergency: espeak

text

## 📊 **Performance**

- **Response Time**: 2-5 seconds for complete voice-to-voice interaction
- **Knowledge Base**: 60+ professionally sourced historical facts
- **Conversation Memory**: Tracks last 3 exchanges per session
- **Voice Generation**: Multi-provider reliability with automatic fallback
- **Concurrent Users**: Optimized for multiple simultaneous conversations

## 🧪 **Testing**

### **Run comprehensive tests:**
```bash
# Test all systems
python test_enhanced_systems.py

# Test voice integration specifically
python test_tts_integration.py

# Test conversation memory
python test_memory_system.py
```

### **Manual testing:**
```bash
# Quick character voice test
python quick_tts_test.py
```

## 📁 **Project Structure**

```
Backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── api/
│   │   └── dialogue.py            # Main conversation endpoints
│   ├── core/
│   │   ├── stt.py                 # Speech-to-Text service
│   │   ├── rag.py                 # Knowledge retrieval system
│   │   ├── llm.py                 # Language model integration
│   │   ├── tts.py                 # Text-to-Speech service
│   │   └── session_manager.py     # Conversation memory
│   ├── models/
│   │   └── dialogue.py            # API request/response models
│   ├── data/
│   │   └── enhanced_historical_facts.py  # Historical knowledge base
│   └── utils/
│       └── knowledge_seeder.py    # Database initialization
├── generated_audio/               # TTS output directory
├── knowledge_db/                  # ChromaDB storage
├── testing/                       # Test files
├── Docs/                          # Documentation
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```
text

## 🔧 **Configuration**

### **Environment Variables**
Create `.env` file with:
```env
OLLAMA_HOST=http://127.0.0.1:12345
OLLAMA_MODEL=llama3.2:3b
STT_MODEL_SIZE=base
CHROMA_PERSIST_DIRECTORY=./knowledge_db
```

### **Ollama Optimization**
```bash
export OLLAMA_NUM_PARALLEL=6
export OLLAMA_CONTEXT_LENGTH=1024
export OLLAMA_KEEP_ALIVE=15m
```
text

## 🎓 **Educational Use Cases**

- **History Education**: Interactive learning with historical figures
- **Museum Exhibits**: Voice-guided historical experiences  
- **Language Learning**: Historical context for language instruction
- **Academic Research**: Historically accurate dialogue generation
- **Cultural Preservation**: Digital preservation of historical knowledge

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-character`)
3. Implement your changes
4. Add comprehensive tests
5. Submit a pull request

### **Adding New Characters**
1. Add historical facts to `enhanced_historical_facts.py`
2. Update character personas in `llm.py`
3. Configure voice settings in `tts.py`
4. Add character info to `dialogue.py`
5. Run knowledge seeder: `python -m app.utils.knowledge_seeder`

## 📚 **Documentation**

- **API Documentation**: `http://localhost:8000/docs` (Interactive)
- **Technical Architecture**: See `docs/architecture.md`
- **Historical Accuracy**: See `docs/historical_sources.md`
- **Development Guide**: See `docs/development.md`

## 🐛 **Troubleshooting**

### **Common Issues**

**Ollama Connection Failed:**
```bash
# Check Ollama is running on correct port
curl http://127.0.0.1:12345/api/tags

# Restart Ollama if needed
ollama serve
```

**No Audio Generated:**
```bash
# Check TTS service status
curl http://localhost:8000/api/v1/tts/info

# Check generated_audio directory permissions
ls -la generated_audio/
```

**Knowledge Base Empty:**
```bash
# Re-initialize knowledge base
python -m app.utils.knowledge_seeder
```

## 🔄 **Integration with GameClient**

### **API Communication**
The backend provides RESTful APIs that the Unreal Engine 5 client uses for:
- **Real-time dialogue** with historical characters
- **Voice processing** (STT/TTS) for immersive interactions
- **Knowledge retrieval** for historically accurate responses
- **Session management** for conversation continuity

### **Data Flow**
```
UE5 Client → HTTP Request → FastAPI Backend → AI Processing → Response → UE5 Client
```

### **Performance Optimization**
- **Async processing** for non-blocking operations
- **Connection pooling** for efficient resource usage
- **Caching strategies** for frequently accessed data
- **Load balancing** ready for multiple backend instances

## 📈 **Roadmap**

### **Phase 1 - Core Features** ✅
- [x] Basic AI backend with 4 historical characters
- [x] Speech recognition and synthesis
- [x] Knowledge retrieval system
- [x] UE5 client integration

### **Phase 2 - Enhancement** 🚧
- [ ] Additional historical characters (Medieval King, Renaissance Artist)
- [ ] Multi-language support
- [ ] Advanced conversation memory
- [ ] Real-time streaming audio

### **Phase 3 - Advanced Features** 📋
- [ ] AI-powered character customization
- [ ] Educational analytics and tracking
- [ ] Multi-user session management
- [ ] Advanced RAG with multiple knowledge sources

## 🔧 **Technical Specifications**

### **System Requirements**
- **CPU**: Multi-core processor (Intel i5/AMD Ryzen 5 or better)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for models and database
- **Network**: Internet connection for TTS services
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+

### **AI Model Specifications**
- **LLM**: llama3.2:3b (3 billion parameters)
- **STT**: OpenAI Whisper base model (39M parameters)
- **Embeddings**: all-MiniLM-L6-v2 (23M parameters)
- **Vector DB**: ChromaDB with persistent storage

### **Performance Benchmarks**
- **Response Time**: 2-5 seconds end-to-end
- **Concurrent Users**: 10+ simultaneous conversations
- **Memory Usage**: ~2GB RAM for full stack
- **Storage**: ~500MB for models + knowledge base

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Historical Consultants**: For accuracy verification and source validation
- **OpenAI**: For Whisper speech recognition technology
- **Ollama**: For local LLM inference capabilities
- **ChromaDB**: For vector database and embedding storage
- **FastAPI**: For high-performance API framework
- **Unreal Engine**: For 3D graphics and game development platform

## 📞 **Support & Community**

- **Documentation**: Check the `Docs/` directory for detailed guides
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join community discussions for help
- **Contributing**: See development guide in `Docs/development.md`

---

**Built with ❤️ for historical education and AI innovation**

*Bringing history to life through artificial intelligence* 🏛️✨
