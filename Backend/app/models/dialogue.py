from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DialogueRequest(BaseModel):
    character_id: str = Field(
        ..., 
        description="ID of the historical character (e.g., 'roman_gladiator')",
        example="roman_gladiator"
    )
    scene_context: str = Field(
        default="general", 
        description="Current scene/location context",
        example="colosseum_training_grounds"
    )
    user_text: Optional[str] = Field(
        None, 
        description="Direct text input (we'll add audio later)",
        example="Tell me about gladiator training"
    )

class DialogueResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    transcript: str = Field(..., description="What the user said (or typed)")
    response_text: str = Field(..., description="Character's response")
    character_id: str = Field(..., description="Which character responded")
    scene_context: str = Field(..., description="Current scene context")
    processing_time_ms: int = Field(..., description="How long it took to process")
    audio_url: Optional[str] = Field(None, description="URL to audio file (coming later)")
    session_id: Optional[str] = None
    
class ErrorResponse(BaseModel):
    success: bool = Field(default=False)
    error: str = Field(..., description="What went wrong")
    timestamp: datetime = Field(default_factory=datetime.now)