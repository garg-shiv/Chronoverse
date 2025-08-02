# Development Guide - Chronoverse Backend

## Development Environment Setup

### Prerequisites
- Python 3.13+
- Git
- Ollama
- Audio system (for TTS testing)

### Initial Setup
Clone repository
git clone <repository-url>
cd Chronoverse/Backend

Create virtual environment
python -m venv chronoverse_env
source chronoverse_env/bin/activate # Unix

chronoverse_env\Scripts\Activate.ps1 # Windows
Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt # Development tools

text

### Ollama Setup
Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh # Unix

Download from https://ollama.ai for Windows
Configure custom port
export OLLAMA_HOST=http://127.0.0.1:12345

Start Ollama
ollama serve

Pull required model
ollama pull llama3.2:3b

text

## Project Structure Deep Dive

Backend/
├── app/
│ ├── init.py # Package initialization
│ ├── main.py # FastAPI app and startup
│ ├── api/
│ │ ├── init.py
│ │ └── dialogue.py # Main API endpoints
│ ├── core/ # Core business logic
│ │ ├── init.py
│ │ ├── stt.py # Speech-to-Text service
│ │ ├── rag.py # Retrieval-Augmented Generation
│ │ ├── llm.py # Language Model service
│ │ ├── tts.py # Text-to-Speech service
│ │ └── session_manager.py # Conversation memory
│ ├── models/ # Pydantic models
│ │ ├── init.py
│ │ └── dialogue.py # Request/Response models
│ ├── data/ # Static data and configuration
│ │ ├── init.py
│ │ └── enhanced_historical_facts.py
│ └── utils/ # Utility functions
│ ├── init.py
│ └── knowledge_seeder.py # Database initialization
├── generated_audio/ # TTS output files
├── knowledge_db/ # ChromaDB persistent storage
├── tests/ # Test files
├── docs/ # Documentation
├── requirements.txt # Production dependencies
├── requirements-dev.txt # Development dependencies
└── README.md # Main documentation

text

## Adding New Historical Characters

### Step 1: Define Historical Facts
Add to `app/data/enhanced_historical_facts.py`:

"new_character_id": {
"character_info": {
"name": "Character Name",
"period": "Time Period",
"background": "Historical background"
},
"facts": [
{
"text": "Detailed historical fact...",
"category": "category_name",
"subcategory": "subcategory",
"historical_accuracy": "high",
"source": "Historical source citation"
},
# Add 15+ facts per character
]
}

text

### Step 2: Add Character Persona
Update `app/core/llm.py` character_personas:

"new_character_id": {
"name": "Character Name",
"role": "Historical role",
"personality": "Personality description",
"speech_style": "Speaking style and mannerisms",
"background": "Detailed background",
"expertise": ["area1", "area2", "area3"],
"greeting_style": "How they greet people"
}

text

### Step 3: Configure Voice
Update `app/core/tts.py` character voices:

"new_character_id": {
"voice": "VoiceName",
"speed": 0.8,
"pitch": 0,
"style": "voice style description"
}

text

### Step 4: Add Character Info
Update `app/api/dialogue.py` CHARACTERS:

"new_character_id": {
"name": "Character Name",
"title": "Character Title",
"greeting": "Character greeting message",
"personality": "Brief personality description"
}

text

### Step 5: Initialize Knowledge Base
python -m app.utils.knowledge_seeder

text

### Step 6: Test New Character
python test_new_character.py

text

## Development Workflow

### Code Style
Format code
black app/ tests/

Check linting
flake8 app/ tests/

Type checking
mypy app/

text

### Testing
Run all tests
pytest

Run specific test file
pytest tests/test_dialogue.py

Run with coverage
pytest --cov=app tests/

text

### Git Workflow
Create feature branch
git checkout -b feature/new-character-name

Make changes and commit
git add .
git commit -m "feat: add new historical character"

Push and create PR
git push origin feature/new-character-name

text

## Debugging

### Logging Configuration
import logging

Set log level in main.py
logging.basicConfig(level=logging.INFO)

Add debug logging in your code
logger = logging.getLogger(name)
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")

text

### Common Debug Commands
Check Ollama status
curl http://127.0.0.1:12345/api/tags

Test API endpoints
curl -X POST "http://localhost:8000/api/v1/dialogue"
-H "Content-Type: application/x-www-form-urlencoded"
-d "character_id=roman_gladiator&user_text=Hello"

Check ChromaDB
python -c "import chromadb; print(chromadb.Client().list_collections())"

Monitor audio files
ls -la generated_audio/

text

### Performance Profiling
import cProfile
import pstats

Profile a function
cProfile.run('your_function()', 'profile_output')
stats = pstats.Stats('profile_output')
stats.sort_stats('tottime').print_stats(10)

text

## Testing Guidelines

### Unit Tests
import pytest
from app.core.llm import get_llm_service

@pytest.mark.asyncio
async def test_character_response():
llm_service = get_llm_service()
response = await llm_service.generate_simple_response(
character_id="roman_gladiator",
user_query="Hello"
)
assert response["success"] == True
assert "Marcus" in response["response_text"]

text

### Integration Tests  
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dialogue_endpoint():
response = client.post("/api/v1/dialogue", data={
"character_id": "roman_gladiator",
"user_text": "Tell me about training"
})
assert response.status_code == 200
assert "audio_url" in response.json()

text

### Performance Tests
import time

def test_response_time():
start = time.time()
# Your API call here
duration = time.time() - start
assert duration < 10.0 # Max 10 seconds

text

## Deployment Preparation

### Environment Variables
Create production `.env`:
ENVIRONMENT=production
OLLAMA_HOST=http://ollama-service:11434
LOG_LEVEL=INFO
CORS_ORIGINS=["https://your-frontend.com"]

text

### Docker Configuration
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
COPY knowledge_db/ ./knowledge_db/

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

text

### Health Checks
Add to main.py
@app.get("/health")
async def health_check():
return {
"status": "healthy",
"timestamp": datetime.now().isoformat(),
"services": {
"ollama": check_ollama_health(),
"chromadb": check_chromadb_health(),
"tts": check_tts_health()
}
}

text

## Contribution Guidelines

### Code Standards
- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write docstrings for all public methods
- Maintain test coverage > 80%

### Pull Request Process
1. Create feature branch from main
2. Implement changes with tests
3. Update documentation
4. Submit PR with clear description
5. Address review feedback
6. Merge after approval

### Issue Reporting
Include in bug reports:
- Python version and OS
- Error messages and stack traces
- Steps to reproduce
- Expected vs actual behavior
- Relevant log output

---

Happy coding! 🚀
