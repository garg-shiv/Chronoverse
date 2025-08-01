import whisper
import logging
from typing import Optional
import torch
import librosa
import numpy as np
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhisperSTT:
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"🎤 Initializing Whisper STT with model: {model_size} on device: {self.device}")
        self._load_model()

    def _load_model(self):
        try:
            logger.info(f"📥 Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size, device=self.device)
            logger.info("✅ Whisper model loaded successfully!")
        except Exception as e:
            logger.error(f"❌ Failed to load Whisper model: {e}")
            raise Exception(f"Could not initialize Whisper: {e}")

    async def transcribe_audio(self, audio_data: bytes, language: str = None) -> dict:
        if not self.model:
            raise Exception("Whisper model not loaded!")
        
        try:
            logger.info(f"🎵 Processing {len(audio_data)} bytes of audio data in memory")
            
            audio_array, sample_rate = librosa.load(
                io.BytesIO(audio_data), 
                sr=16000
            )
            
            logger.info(f"🔄 Loaded audio: {len(audio_array)} samples at {sample_rate}Hz")
            
            if len(audio_array.shape) > 1:
                audio_array = librosa.to_mono(audio_array)
            
            audio_array = audio_array.astype(np.float32)
            
            logger.info(f"🎯 Transcribing audio array directly...")
            
            if language:
                result = self.model.transcribe(audio_array, language=language)
            else:
                result = self.model.transcribe(audio_array)
            
            transcript = result["text"].strip()
            language_detected = result.get("language", "unknown")
            
            logger.info(f"✅ Transcription successful: '{transcript}' (Language: {language_detected})")
            
            return {
                "transcript": transcript,
                "language": language_detected,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"❌ Transcription failed: {e}")
            return {
                "transcript": "",
                "language": "unknown",
                "success": False,
                "error": str(e)
            }

    def get_model_info(self) -> dict:
        return {
            "model_size": self.model_size,
            "device": self.device,
            "is_loaded": self.model is not None,
            "processing_method": "in_memory",
            "supported_formats": ["wav", "mp3", "flac", "ogg", "m4a"]
        }

_stt_instance: Optional[WhisperSTT] = None

def get_stt_service() -> WhisperSTT:
    global _stt_instance
    if _stt_instance is None:
        _stt_instance = WhisperSTT(model_size="base")
    return _stt_instance