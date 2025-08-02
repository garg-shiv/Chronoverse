import requests
import os
import logging
import time
from typing import Dict, Optional
from datetime import datetime
import json
import tempfile

logger = logging.getLogger(__name__)

class WorkingFreeTTSService:
    
    def __init__(self):
        self.output_dir = "generated_audio"
        self.character_voices = self._load_character_voice_settings()
        self._ensure_output_directory()
        logger.info("🎤 Working Free TTS Service initialized")
    
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
                "voice": "Matthew",
                "speed": 0.9,
                "pitch": -20,
                "style": "commanding and authoritative"
            },
            "mughal_architect": {
                "voice": "Brian", 
                "speed": 0.8,
                "pitch": 0,
                "style": "wise and contemplative"
            },
            "egyptian_scribe": {
                "voice": "Russell",
                "speed": 0.7,
                "pitch": 10,
                "style": "scholarly and formal"
            },
            "medieval_knight": {
                "voice": "Matthew",
                "speed": 0.85,
                "pitch": -10,
                "style": "noble and honorable"
            },
            "viking_explorer": {
                "voice": "Matthew",
                "speed": 0.85,
                "pitch": -15,
                "style": "bold and adventurous"
            },
            "renaissance_master": {
                "voice": "Brian",
                "speed": 0.8,
                "pitch": 5,
                "style": "curious and brilliant"
            }
        }
    
    async def generate_character_speech(
        self, 
        character_id: str, 
        text: str, 
        session_id: Optional[str] = None
    ) -> Dict[str, str]:
        
        if character_id not in self.character_voices:
            logger.error(f"❌ Unknown character: {character_id}")
            return {
                "success": False,
                "error": f"Unknown character: {character_id}",
                "character_id": character_id
            }
        
        if not text or not text.strip():
            logger.error("❌ Empty text provided for TTS")
            return {
                "success": False,
                "error": "Text cannot be empty",
                "character_id": character_id
            }
        
        if len(text) > 500:
            text = text[:497] + "..."
            logger.warning(f"⚠️ Text truncated to 500 characters for {character_id}")
        
        voice_config = self.character_voices[character_id]
        start_time = time.time()
        
        tts_services = [
            self._try_streamelements_tts,
            self._try_voicerss_tts,
            self._try_espeak_tts
        ]
        
        for i, tts_service in enumerate(tts_services, 1):
            logger.info(f"🎭 Trying TTS service {i} for {character_id}")
            
            result = await tts_service(character_id, text, voice_config, session_id)
            
            if result["success"]:
                generation_time = int((time.time() - start_time) * 1000)
                result["generation_time_ms"] = generation_time
                result["voice_style"] = voice_config["style"]
                
                logger.info(f"✅ Generated speech for {character_id} in {generation_time}ms using service {i}")
                return result
            else:
                logger.warning(f"⚠️ TTS service {i} failed: {result.get('error')}")
        
        generation_time = int((time.time() - start_time) * 1000)
        return {
            "success": False,
            "error": "All TTS services failed",
            "character_id": character_id,
            "generation_time_ms": generation_time
        }
    
    async def _try_streamelements_tts(self, character_id: str, text: str, voice_config: Dict, session_id: Optional[str]) -> Dict:
        try:
            response = requests.get(
                "https://api.streamelements.com/kappa/v2/speech",
                params={
                    "voice": voice_config["voice"],
                    "text": text
                },
                timeout=30
            )
            
            if response.status_code == 200 and len(response.content) > 1000:
                return self._save_audio_file(response.content, character_id, session_id, "streamelements", "mp3")
            else:
                return {"success": False, "error": f"StreamElements API error: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": f"StreamElements error: {str(e)}"}
    
    async def _try_voicerss_tts(self, character_id: str, text: str, voice_config: Dict, session_id: Optional[str]) -> Dict:
        try:
            response = requests.get(
                "http://api.voicerss.org/",
                params={
                    "key": "demo",
                    "hl": "en-us",
                    "src": text,
                    "f": "44khz_16bit_stereo",
                    "c": "mp3"
                },
                timeout=30
            )
            
            if response.status_code == 200 and len(response.content) > 1000:
                return self._save_audio_file(response.content, character_id, session_id, "voicerss", "mp3")
            else:
                return {"success": False, "error": f"VoiceRSS API error: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": f"VoiceRSS error: {str(e)}"}
    
    async def _try_espeak_tts(self, character_id: str, text: str, voice_config: Dict, session_id: Optional[str]) -> Dict:
        try:
            import subprocess
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            session_part = f"_{session_id[:8]}" if session_id else ""
            audio_filename = f"{character_id}_{timestamp}_espeak{session_part}.wav"
            audio_path = os.path.join(self.output_dir, audio_filename)
            
            cmd = [
                "espeak",
                "-s", str(int(voice_config["speed"] * 200)),
                "-w", audio_path,
                text
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                return {
                    "success": True,
                    "audio_url": f"/audio/{audio_filename}",
                    "audio_path": audio_path,
                    "character_id": character_id,
                    "provider": "espeak (local)"
                }
            else:
                return {"success": False, "error": "espeak command failed"}
                
        except Exception as e:
            return {"success": False, "error": f"espeak error: {str(e)}"}
    
    def _save_audio_file(self, audio_content: bytes, character_id: str, session_id: Optional[str], provider: str, extension: str) -> Dict:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            session_part = f"_{session_id[:8]}" if session_id else ""
            audio_filename = f"{character_id}_{timestamp}_{provider}{session_part}.{extension}"
            audio_path = os.path.join(self.output_dir, audio_filename)
            
            with open(audio_path, "wb") as f:
                f.write(audio_content)
            
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                return {
                    "success": True,
                    "audio_url": f"/audio/{audio_filename}",
                    "audio_path": audio_path,
                    "character_id": character_id,
                    "provider": provider,
                    "file_size": os.path.getsize(audio_path)
                }
            else:
                return {"success": False, "error": f"Failed to save audio file from {provider}"}
                
        except Exception as e:
            return {"success": False, "error": f"File save error: {str(e)}"}
    
    def get_system_info(self) -> Dict:
        return {
            "tts_provider": "Free TTS Services",
            "services": ["StreamElements", "VoiceRSS", "espeak"],
            "api_configured": True,
            "output_directory": self.output_dir,
            "available_characters": len(self.character_voices),
            "character_voices": list(self.character_voices.keys()),
            "features": [
                "No API key required",
                "Multiple service fallbacks", 
                "Character-specific voices",
                "Fast generation"
            ]
        }
    
    def get_character_voice_info(self, character_id: str) -> Dict:
        if character_id not in self.character_voices:
            return {"success": False, "error": f"Unknown character: {character_id}"}
        
        config = self.character_voices[character_id]
        return {
            "success": True,
            "character_id": character_id,
            "voice": config["voice"],
            "style": config["style"],
            "speed": config["speed"],
            "pitch": config["pitch"]
        }

_tts_instance: Optional[WorkingFreeTTSService] = None

def get_tts_service() -> WorkingFreeTTSService:
    global _tts_instance
    if _tts_instance is None:
        _tts_instance = WorkingFreeTTSService()
    return _tts_instance
