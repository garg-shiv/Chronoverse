from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Dict, Optional
import time
from datetime import datetime
import logging

from ..models.dialogue import DialogueRequest, DialogueResponse, ErrorResponse
from ..core.stt import get_stt_service
from ..core.rag import get_rag_service
from ..core.llm import get_llm_service

logger = logging.getLogger(__name__)

router = APIRouter()

CHARACTERS = {
    "roman_gladiator": {
        "name": "Marcus Quintus",
        "title": "Gladiator of the Colosseum",
        "greeting": "Salve, citizen! I am Marcus, a gladiator who has fought in the great arena.",
        "personality": "Brave, disciplined, speaks with authority about combat and honor"
    },
    "mughal_architect": {
        "name": "Ustad Ahmad Lahauri",
        "title": "Master Architect",
        "greeting": "Peace be upon you. I am Ahmad, architect of magnificent monuments.",
        "personality": "Wise, artistic, speaks about beauty, mathematics, and divine inspiration"
    },
    "egyptian_scribe": {
        "name": "Khaemwaset",
        "title": "Royal Scribe",
        "greeting": "Greetings, traveler. I serve in the house of Pharaoh as keeper of sacred knowledge.",
        "personality": "Learned, formal, speaks about hieroglyphs, gods, and ancient wisdom"
    }
}

def should_use_rag(user_input: str) -> bool:
    rag_keywords = [
        "when", "where", "how", "why", "what", "built", "made", "during",
        "training", "weapon", "fight", "battle", "construction", "material",
        "technique", "year", "time", "happened", "did you", "were you",
        "tell me about", "explain", "describe", "history", "ancient",
        "combat", "arena", "gladiator", "architect", "scribe", "pharaoh"
    ]
    
    conversational_keywords = [
        "hello", "hi", "thanks", "thank you", "interesting", "nice", "cool",
        "good", "okay", "yes", "no", "who are you", "nice to meet",
        "how are you", "goodbye", "bye"
    ]
    
    user_lower = user_input.lower()
    
    if any(keyword in user_lower for keyword in conversational_keywords):
        return False
    
    if any(keyword in user_lower for keyword in rag_keywords):
        return True
    
    if len(user_input.strip()) < 20:
        return False
    
    return True

async def generate_rag_enhanced_response(user_input: str, character_id: str, scene_context: str) -> str:
    try:
        start_rag = time.time()
        rag_service = get_rag_service()
        historical_facts = await rag_service.retrieve_relevant_facts(
            character_id=character_id,
            query=user_input,
            max_results=3
        )
        rag_time = time.time() - start_rag
        
        start_llm = time.time()
        llm_service = get_llm_service()
        response_data = await llm_service.generate_response(
            character_id=character_id,
            user_query=user_input,
            historical_facts=historical_facts
        )
        llm_time = time.time() - start_llm
        
        logger.info(f"📚 RAG + LLM response: RAG {rag_time:.2f}s, LLM {llm_time:.2f}s")
        return response_data["response_text"]
        
    except Exception as e:
        logger.error(f"❌ RAG-enhanced response failed: {e}")
        character = CHARACTERS.get(character_id, {})
        return character.get("greeting", "I apologize, but I'm having trouble responding right now.")

async def generate_conversational_response(user_input: str, character_id: str, scene_context: str) -> str:
    try:
        start_llm = time.time()
        llm_service = get_llm_service()
        response_data = await llm_service.generate_simple_response(
            character_id=character_id,
            user_query=user_input
        )
        llm_time = time.time() - start_llm
        
        logger.info(f"💬 LLM-only response: {llm_time:.2f}s")
        return response_data["response_text"]
        
    except Exception as e:
        logger.error(f"❌ Conversational response failed: {e}")
        character = CHARACTERS.get(character_id, {})
        return character.get("greeting", "Hello! I'd be happy to share my knowledge with you.")

async def generate_adaptive_response(user_input: str, character_id: str, scene_context: str) -> str:
    needs_historical_facts = should_use_rag(user_input)
    
    if needs_historical_facts:
        logger.info(f"🔍 Using RAG + LLM for: '{user_input[:50]}...'")
        return await generate_rag_enhanced_response(user_input, character_id, scene_context)
    else:
        logger.info(f"💬 Using LLM-only for: '{user_input[:50]}...'")
        return await generate_conversational_response(user_input, character_id, scene_context)

@router.post("/dialogue", response_model=DialogueResponse)
async def create_dialogue(
    character_id: str = Form(...),
    scene_context: str = Form(default="general"),
    audio_file: Optional[UploadFile] = File(None),
    user_text: Optional[str] = Form(None)
):
    start_time = time.time()
    
    try:
        if character_id not in CHARACTERS:
            raise HTTPException(
                status_code=400, 
                detail=f"Unknown character: {character_id}. Available: {list(CHARACTERS.keys())}"
            )
        
        character = CHARACTERS[character_id]
        transcript = ""
        
        if audio_file:
            logger.info(f"🎤 Processing audio file: {audio_file.filename}")
            
            audio_data = await audio_file.read()
            
            if len(audio_data) == 0:
                raise HTTPException(status_code=400, detail="Empty audio file received")
            
            stt_service = get_stt_service()
            stt_result = await stt_service.transcribe_audio(audio_data)
            
            if not stt_result["success"]:
                raise HTTPException(
                    status_code=422, 
                    detail=f"Could not transcribe audio: {stt_result.get('error', 'Unknown error')}"
                )
            
            transcript = stt_result["transcript"]
            logger.info(f"🎯 Transcribed: '{transcript}'")
            
        elif user_text:
            transcript = user_text
            logger.info(f"💬 Text input: '{transcript}'")
            
        else:
            raise HTTPException(
                status_code=400, 
                detail="Either audio_file or user_text must be provided"
            )
        
        if transcript.strip():
            response_text = await generate_adaptive_response(transcript, character_id, scene_context)
        else:
            response_text = character["greeting"]
        
        processing_time = int((time.time() - start_time) * 1000)
        
        logger.info(f"✅ Complete dialogue processing finished in {processing_time}ms")
        
        return DialogueResponse(
            success=True,
            transcript=transcript,
            response_text=response_text,
            character_id=character_id,
            scene_context=scene_context,
            processing_time_ms=processing_time,
            audio_url=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = int((time.time() - start_time) * 1000)
        logger.error(f"❌ Dialogue processing failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/characters")
async def list_characters():
    return {
        "characters": CHARACTERS,
        "count": len(CHARACTERS)
    }

@router.get("/stt/info")
async def get_stt_info():
    try:
        stt_service = get_stt_service()
        return stt_service.get_model_info()
    except Exception as e:
        return {"error": str(e), "is_loaded": False}

@router.get("/llm/info")
async def get_llm_info():
    try:
        llm_service = get_llm_service()
        return llm_service.get_model_info()
    except Exception as e:
        return {"error": str(e), "status": "unavailable"}
