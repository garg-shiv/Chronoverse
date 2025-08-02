# Chronoverse - AI-Powered Historical Education Platform 🏛️

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Unreal Engine](https://img.shields.io/badge/Unreal%20Engine-5.3-orange.svg)](https://unrealengine.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)
[![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)]()
[![Voice Enabled](https://img.shields.io/badge/Voice-Enabled-orange.svg)]()

**Chronoverse** is an innovative AI-powered platform that brings history to life through immersive conversations with historically accurate characters. Combining advanced speech recognition, knowledge retrieval, and voice synthesis with Unreal Engine 5 graphics, it creates an unparalleled educational experience.

## 🌟 **Project Overview**

Chronoverse consists of two main components:

- **🎭 Backend AI Engine** - Sophisticated AI backend with speech processing, knowledge retrieval, and voice synthesis
- **🎮 GameClient (UE5)** - Immersive 3D environment with historical characters and interactive experiences

## 🏗️ **Architecture**

```
Chronoverse/
├── Backend/                 # AI-Powered Backend Engine
│   ├── app/                # FastAPI application
│   ├── knowledge_db/       # ChromaDB vector database
│   ├── generated_audio/    # TTS output files
│   └── Docs/              # Technical documentation
├── GameClient/             # Unreal Engine 5 Client
│   ├── Content/           # 3D assets and blueprints
│   ├── Source/            # C++ source code
│   └── Plugins/           # Custom UE5 plugins
```

## 🎭 **Historical Characters**

### **Marcus Quintus** - Roman Gladiator (1st-2nd Century CE)
- **Expertise**: Gladiatorial combat, Roman society, military training
- **Voice**: Deep, commanding with Latin accent
- **Personality**: Proud, disciplined, honorable warrior

### **Ustad Ahmad Lahauri** - Mughal Architect (17th Century CE)
- **Expertise**: Islamic architecture, Taj Mahal construction, geometric design
- **Voice**: Wise, measured with Persian accent
- **Personality**: Patient, detail-oriented, spiritually minded

### **Khaemwaset** - Egyptian Royal Scribe (New Kingdom, 19th Dynasty)
- **Expertise**: Hieroglyphics, Egyptian administration, temple rituals
- **Voice**: Formal, precise with ancient Egyptian accent
- **Personality**: Scholarly, respectful, deeply traditional

### **Sir Gareth** - Medieval Knight (14th Century CE)
- **Expertise**: Chivalry, medieval warfare, castle life
- **Voice**: Noble, chivalrous with medieval English accent
- **Personality**: Honorable, brave, courtly manners

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.13+
- Unreal Engine 5.3+
- Ollama with llama3.2:3b model
- Windows/Linux/macOS

### **Backend Setup**

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

### **GameClient Setup**

1. **Open in Unreal Engine 5:**
```bash
cd Chronoverse/GameClient
# Open Chronoverse.uproject in UE5
```

2. **Install required plugins:**
- VoiceComm plugin (included in Plugins/)
- Any additional marketplace assets

3. **Configure backend connection:**
- Update API endpoints in VoiceCommComponent
- Set backend server URL in GameInstanceSubsystem

## 📡 **API Documentation**

### **Core Endpoints**
- `POST /api/v1/dialogue` - Main conversation endpoint
- `GET /api/v1/characters` - List available characters
- `GET /health` - System health check

### **Service Information**
- `GET /api/v1/stt/info` - Speech-to-Text service status
- `GET /api/v1/llm/info` - Language model information
- `GET /api/v1/tts/info` - Text-to-Speech service details

### **Example Usage**

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

## 🎮 **GameClient Features**

### **3D Environments**
- **Colosseum** - Roman gladiatorial arena
- **Humayun's Tomb** - Mughal architectural masterpiece
- **Egyptian Temple** - Ancient scribal chambers
- **Medieval Castle** - Knightly training grounds

### **Interactive Elements**
- **Voice Recognition** - Real-time speech input
- **Character Animation** - Lifelike historical figures
- **Environmental Audio** - Immersive soundscapes
- **UI Integration** - Seamless conversation interface

### **Technical Implementation**
- **C++ Backend** - High-performance game systems
- **Blueprint Integration** - Visual scripting for interactions
- **VoiceComm Plugin** - Custom voice communication system
- **Historical Accuracy** - Authentic period-appropriate assets

## 🤖 **AI Technologies**

### **Speech Processing**
- **Speech-to-Text**: OpenAI Whisper for voice input
- **Text-to-Speech**: Multi-service TTS with character voices
- **Voice Recognition**: Real-time audio processing

### **Knowledge System**
- **RAG (Retrieval-Augmented Generation)**: ChromaDB with vector search
- **Language Model**: Ollama with llama3.2:3b for dialogue
- **Historical Facts**: 60+ professionally sourced facts per character

### **Conversation Memory**
- **Session Management**: Context-aware conversations
- **Memory Tracking**: Last 3 exchanges per session
- **Character Consistency**: Personality and knowledge persistence

## 📊 **Performance Metrics**

- **Response Time**: 2-5 seconds for complete voice-to-voice interaction
- **Knowledge Base**: 60+ professionally sourced historical facts per character
- **Voice Generation**: Multi-provider reliability with automatic fallback
- **3D Rendering**: Optimized for 60 FPS on recommended hardware
- **Concurrent Users**: Scalable architecture for multiple simultaneous users

## 🧪 **Testing**

### **Backend Testing**
```bash
# Run comprehensive tests
python test_enhanced_systems.py

# Test voice integration
python test_tts_integration.py

# Test conversation memory
python test_memory_system.py
```

### **GameClient Testing**
- **Voice Integration Tests** - Verify speech recognition and TTS
- **Performance Tests** - Frame rate and memory usage
- **UI/UX Tests** - User interface functionality
- **Multiplayer Tests** - Concurrent user scenarios

## 📁 **Project Structure**

```
Chronoverse/
├── Backend/
│   ├── app/
│   │   ├── api/           # FastAPI endpoints
│   │   ├── core/          # AI services (STT, RAG, LLM, TTS)
│   │   ├── data/          # Historical facts and knowledge
│   │   ├── models/        # Pydantic models
│   │   └── utils/         # Utility functions
│   ├── knowledge_db/      # ChromaDB storage
│   ├── generated_audio/   # TTS output
│   ├── testing/           # Test files
│   └── Docs/              # Documentation
├── GameClient/
│   ├── Content/
│   │   ├── Audio/         # Sound effects and music
│   │   ├── Blueprints/    # Visual scripting
│   │   ├── Characters/    # 3D character models
│   │   ├── Environments/  # 3D environments
│   │   └── UI/           # User interface
│   ├── Source/
│   │   └── Chronoverse/   # C++ source code
│   └── Plugins/
│       └── VoiceComm/     # Custom voice plugin

```

## 🔧 **Configuration**

### **Environment Variables**
Create `.env` file in Backend directory:
```env
OLLAMA_HOST=http://127.0.0.1:12345
OLLAMA_MODEL=llama3.2:3b
STT_MODEL_SIZE=base
CHROMA_PERSIST_DIRECTORY=./knowledge_db
```

### **Unreal Engine Settings**
- **Rendering**: Optimized for historical accuracy
- **Audio**: High-quality voice processing
- **Networking**: Backend API integration
- **Performance**: Balanced quality and performance

## 🎓 **Educational Applications**

### **Classroom Integration**
- **History Education**: Interactive learning with historical figures
- **Language Learning**: Historical context for language instruction
- **Cultural Studies**: Immersive cultural experiences
- **Museum Exhibits**: Voice-guided historical experiences

### **Academic Use Cases**
- **Research Tool**: Historically accurate dialogue generation
- **Cultural Preservation**: Digital preservation of historical knowledge
- **Distance Learning**: Remote historical education
- **Special Education**: Accessible historical learning

## 🤝 **Contributing**

### **Development Workflow**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-character`)
3. Implement your changes with comprehensive tests
4. Update documentation
5. Submit a pull request

### **Adding New Characters**
1. Add historical facts to `Backend/app/data/enhanced_historical_facts.py`
2. Update character personas in `Backend/app/core/llm.py`
3. Configure voice settings in `Backend/app/core/tts.py`
4. Create 3D character model in `GameClient/Content/Characters/`
5. Add character blueprints and interactions
6. Run knowledge seeder: `python -m app.utils.knowledge_seeder`

### **Code Standards**
- Follow PEP 8 for Python code
- Use Unreal Engine coding standards for C++
- Write comprehensive tests for all features
- Maintain documentation for all changes

## 📚 **Documentation**

- **API Documentation**: `http://localhost:8000/docs` (Interactive)
- **Technical Architecture**: `Backend/Docs/Architecture.md`
- **Development Guide**: `Backend/Docs/development.md`
- **Historical Sources**: `Backend/Docs/historical_sources.md`
- **UX/UI Guidelines**: `Backend/Docs/UX_UI_Guidelines.md`

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

**UE5 Compilation Errors:**
- Ensure Visual Studio 2019/2022 is installed
- Check Unreal Engine version compatibility
- Verify all required plugins are enabled

## 📈 **Roadmap**

### **Phase 1 - Core Features** ✅
- [x] Basic AI backend with 4 historical characters
- [x] Speech recognition and synthesis
- [x] Knowledge retrieval system
- [x] UE5 client integration

### **Phase 2 - Enhancement** 🚧
- [ ] Additional historical characters (Medieval King, Renaissance Artist)
- [ ] Multi-language support
- [ ] Advanced 3D character animations
- [ ] Mobile SDK development

### **Phase 3 - Advanced Features** 📋
- [ ] Real-time multiplayer experiences
- [ ] AI-powered character customization
- [ ] Educational dashboard and analytics
- [ ] VR/AR integration

### **Phase 4 - Scale & Deploy** 📋
- [ ] Cloud deployment infrastructure
- [ ] Enterprise educational licensing
- [ ] International localization
- [ ] Advanced AI model integration

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Historical Consultants**: For accuracy verification and source validation
- **OpenAI**: For Whisper speech recognition technology
- **Ollama**: For local LLM inference capabilities
- **ChromaDB**: For vector database and embedding storage
- **FastAPI**: For high-performance API framework
- **Unreal Engine**: For 3D graphics and game development platform

## 📞 **Support**

- **Documentation**: Check the Docs/ directory for detailed guides
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions for help and ideas
- **Email**: Contact the development team for enterprise inquiries

---

**Built with ❤️ for historical education and AI innovation**

*Bringing history to life through artificial intelligence* 🏛️✨

---

<div align="center">

**Chronoverse** - Where History Meets AI

[![GitHub stars](https://img.shields.io/github/stars/your-username/chronoverse?style=social)](https://github.com/your-username/chronoverse)
[![GitHub forks](https://img.shields.io/github/forks/your-username/chronoverse?style=social)](https://github.com/your-username/chronoverse)
[![GitHub issues](https://img.shields.io/github/issues/your-username/chronoverse)](https://github.com/your-username/chronoverse/issues)
[![GitHub license](https://img.shields.io/github/license/your-username/chronoverse)](https://github.com/your-username/chronoverse/blob/main/LICENSE)

</div> 
