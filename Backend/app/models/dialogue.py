from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DialogueRequest(BaseModel):
    character_id: str = Field(..., description="ID of the historical character")
    user_text: Optional[str] = Field(None, description="Text input from user")
    scene_context: str = Field(default="general", description="Scene context for the conversation")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")

class DialogueResponse(BaseModel):
    success: bool
    transcript: str
    response_text: str
    character_id: str
    scene_context: str
    processing_time_ms: int
    audio_url: Optional[str] = None
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class CharacterInfo(BaseModel):
    character_id: str
    name: str
    title: str
    greeting: str
    personality: str

class SystemStatus(BaseModel):
    status: str
    service: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.now)
