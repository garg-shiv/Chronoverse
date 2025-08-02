import pyttsx3
import os
import logging
import queue
import threading
import time
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class HistoricalCharacterTTS:
    def __init__(self):
        self.engine = None
        self.output_dir = "generated_audio"
        self.character_voices = self._load_character_voice_settings()
        self._initialize_engine()
        self._ensure_output_directory()
        logger.info("🎤 Historical Character TTS initialized")

    def _initialize_engine(self):
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            if voices:
                logger.info(f"📋 Available TTS voices: {len(voices)}")
                for i, voice in enumerate(voices[:3]):
                    logger.info(f"   Voice {i}: {voice.name if hasattr(voice, 'name') else 'Unknown'}")
            else:
                logger.warning("⚠️ No TTS voices found on system")
            logger.info("✅ pyttsx3 TTS engine initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize TTS engine: {e}")
            raise Exception(f"TTS engine initialization failed: {e}")

    def _ensure_output_directory(self):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            logger.info(f"📁 Audio output directory ready: {self.output_dir}")
        except Exception as e:
            logger.error(f"❌ Failed to create audio directory: {e}")
            raise

    def _load_character_voice_settings(self) -> Dict[str, Dict]:
        return {
            "roman_gladiator": {
                "name": "Marcus Quintus Voice",
                "voice_index": 0,
                "rate": 160,
                "volume": 1.0,
                "pitch": "normal",
                "style": "commanding and confident"
            },
            "mughal_architect": {
                "name": "Ahmad Lahauri Voice",
                "voice_index": 1,
                "rate": 140,
                "volume": 0.9,
                "pitch": "normal",
                "style": "wise and contemplative"
            },
            "egyptian_scribe": {
                "name": "Khaemwaset Voice", 
                "voice_index": 0,
                "rate": 120,
                "volume": 0.95,
                "pitch": "slightly_higher",
                "style": "scholarly and formal"
            }
        }

    async def generate_character_speech(
        self, 
        character_id: str, 
        text: str, 
        session_id: Optional[str] = None
    ) -> Dict[str, str]:
        if character_id not in self.character_voices:
            logger.error(f"❌ Unknown character voice: {character_id}")
            return {
                "success": False,
                "error": f"Unknown character: {character_id}",
                "character_id": character_id
            }
        
        if not text or not text.strip():
            logger.error(f"❌ Empty text provided for TTS")
            return {
                "success": False,
                "error": "Text cannot be empty",
                "character_id": character_id
            }
        
        try:
            start_time = time.time()
            voice_config = self.character_voices[character_id]
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            session_part = f"_{session_id[:8]}" if session_id else ""
            audio_filename = f"{character_id}_{timestamp}{session_part}.wav"
            audio_path = os.path.join(self.output_dir, audio_filename)
            
            logger.info(f"🎭 Generating speech for {voice_config['name']}: '{text[:50]}...'")
            
            self._configure_character_voice(voice_config)
            
            success = self._generate_speech_file(text, audio_path)
            
            generation_time = int((time.time() - start_time) * 1000)
            
            if success:
                audio_url = f"/audio/{audio_filename}"
                logger.info(f"✅ Speech generated in {generation_time}ms: {audio_url}")
                
                return {
                    "success": True,
                    "audio_url": audio_url,
                    "audio_path": audio_path,
                    "character_id": character_id,
                    "text_length": len(text),
                    "voice_style": voice_config["style"],
                    "generation_time_ms": generation_time,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                logger.error(f"❌ Speech generation failed for {character_id}")
                return {
                    "success": False,
                    "error": "Speech file generation failed",
                    "character_id": character_id,
                    "generation_time_ms": generation_time
                }
                
        except Exception as e:
            generation_time = int((time.time() - start_time) * 1000) if 'start_time' in locals() else 0
            logger.error(f"❌ Speech generation exception for {character_id}: {e}")
            
            return {
                "success": False,
                "error": str(e),
                "character_id": character_id,
                "generation_time_ms": generation_time
            }

    def _configure_character_voice(self, voice_config: Dict):
        try:
            voices = self.engine.getProperty('voices')
            
            if voices and len(voices) > voice_config["voice_index"]:
                selected_voice = voices[voice_config["voice_index"]]
                self.engine.setProperty('voice', selected_voice.id)
                logger.debug(f"🎯 Using voice: {selected_voice.name if hasattr(selected_voice, 'name') else 'Default'}")
            elif voices:
                self.engine.setProperty('voice', voices[0].id)
                logger.debug(f"🎯 Fallback to first voice")
            
            self.engine.setProperty('rate', voice_config["rate"])
            self.engine.setProperty('volume', voice_config["volume"])
            
            logger.debug(f"🔧 Voice configured - Rate: {voice_config['rate']}, Volume: {voice_config['volume']}")
            
        except Exception as e:
            logger.warning(f"⚠️ Voice configuration warning: {e}")

    def _generate_speech_file(self, text: str, output_path: str) -> bool:
        try:
            result_queue = queue.Queue()
            
            def generate_speech():
                try:
                    self.engine.save_to_file(text, output_path)
                    self.engine.runAndWait()
                    result_queue.put(True)
                except Exception as e:
                    logger.error(f"❌ Speech generation thread error: {e}")
                    result_queue.put(False)
            
            speech_thread = threading.Thread(target=generate_speech)
            speech_thread.daemon = True
            speech_thread.start()
            
            speech_thread.join(timeout=30)
            
            if speech_thread.is_alive():
                logger.error("❌ Speech generation timeout")
                return False
            
            try:
                success = result_queue.get_nowait()
                
                if success and os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    if file_size > 0:
                        logger.debug(f"✅ Audio file created: {file_size} bytes")
                        return True
                    else:
                        logger.error("❌ Generated audio file is empty")
                        return False
                else:
                    logger.error("❌ Audio file was not created")
                    return False
                    
            except queue.Empty:
                logger.error("❌ No result from speech generation")
                return False
                
        except Exception as e:
            logger.error(f"❌ Speech file generation failed: {e}")
            return False

    def get_character_voice_info(self, character_id: str) -> Dict:
        if character_id not in self.character_voices:
            return {
                "success": False,
                "error": f"Unknown character: {character_id}",
                "available_characters": list(self.character_voices.keys())
            }
        
        voice_config = self.character_voices[character_id]
        return {
            "success": True,
            "character_id": character_id,
            "voice_name": voice_config["name"],
            "style": voice_config["style"],
            "rate": voice_config["rate"],
            "volume": voice_config["volume"],
            "pitch": voice_config["pitch"]
        }

    def get_system_info(self) -> Dict:
        try:
            voices = self.engine.getProperty('voices') if self.engine else []
            voice_list = []
            
            if voices:
                for i, voice in enumerate(voices):
                    voice_info = {
                        "index": i,
                        "id": voice.id if hasattr(voice, 'id') else f"voice_{i}",
                        "name": voice.name if hasattr(voice, 'name') else f"Voice {i}",
                        "languages": getattr(voice, 'languages', ['en'])
                    }
                    voice_list.append(voice_info)
            
            return {
                "tts_engine": "pyttsx3",
                "engine_loaded": self.engine is not None,
                "python_version_compatible": True,
                "output_directory": self.output_dir,
                "available_characters": len(self.character_voices),
                "character_voices": list(self.character_voices.keys()),
                "system_voices_count": len(voices),
                "system_voices": voice_list,
                "character_voice_configs": {
                    char_id: {
                        "name": config["name"],
                        "style": config["style"],
                        "rate": config["rate"]
                    }
                    for char_id, config in self.character_voices.items()
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting system info: {e}")
            return {
                "tts_engine": "pyttsx3",
                "engine_loaded": False,
                "error": str(e),
                "python_version_compatible": True
            }

    def test_character_voice(self, character_id: str, test_text: str = None) -> Dict:
        if not test_text:
            test_phrases = {
                "roman_gladiator": "Salve, citizen! I am Marcus Quintus, veteran of the arena.",
                "mughal_architect": "Peace be upon you. I am Ahmad, architect of divine beauty.",
                "egyptian_scribe": "Greetings, seeker of wisdom. I am Khaemwaset, keeper of sacred knowledge."
            }
            test_text = test_phrases.get(character_id, "This is a test of the text-to-speech system.")
        
        logger.info(f"🧪 Testing voice for {character_id}")
        return self.generate_character_speech(character_id, test_text)

_tts_instance: Optional[HistoricalCharacterTTS] = None

def get_tts_service() -> HistoricalCharacterTTS:
    global _tts_instance
    if _tts_instance is None:
        _tts_instance = HistoricalCharacterTTS()
    return _tts_instance

async def test_all_character_voices():
    tts_service = get_tts_service()
    
    test_results = {}
    for character_id in ["roman_gladiator", "mughal_architect", "egyptian_scribe"]:
        logger.info(f"🧪 Testing {character_id} voice...")
        result = await tts_service.test_character_voice(character_id)
        test_results[character_id] = result
        
        if result["success"]:
            logger.info(f"✅ {character_id} voice test successful")
        else:
            logger.error(f"❌ {character_id} voice test failed: {result.get('error')}")
    
    return test_results