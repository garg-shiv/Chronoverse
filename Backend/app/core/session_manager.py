import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class ConversationSession:
    def __init__(self, character_id: str, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.character_id = character_id
        self.conversation_history: List[Dict] = []
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.total_exchanges = 0
    
    def add_exchange(self, user_input: str, character_response: str):
        exchange = {
            "user": user_input,
            "character": character_response,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(exchange)
        self.last_activity = datetime.now()
        self.total_exchanges += 1
        
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def get_recent_context(self, max_exchanges: int = 3) -> List[Dict]:
        return self.conversation_history[-max_exchanges:] if self.conversation_history else []
    
    def get_session_duration(self) -> int:
        return int((datetime.now() - self.created_at).total_seconds())
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        return datetime.now() - self.last_activity > timedelta(minutes=timeout_minutes)
    
    def get_conversation_topics(self) -> List[str]:
        topics = []
        for exchange in self.conversation_history:
            user_text = exchange.get("user", "").lower()
            if any(keyword in user_text for keyword in ["battle", "combat", "fight"]):
                topics.append("warfare")
            elif any(keyword in user_text for keyword in ["build", "construct", "design"]):
                topics.append("architecture")
            elif any(keyword in user_text for keyword in ["write", "scroll", "hieroglyph"]):
                topics.append("writing")
            elif any(keyword in user_text for keyword in ["honor", "chivalry", "knight"]):
                topics.append("chivalry")
            elif any(keyword in user_text for keyword in ["sail", "ship", "explore"]):
                topics.append("exploration")
            elif any(keyword in user_text for keyword in ["art", "paint", "invent"]):
                topics.append("renaissance")
        return list(set(topics))

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, ConversationSession] = {}
        self.character_sessions: Dict[str, List[str]] = {}
        logger.info("🧠 Session Manager initialized")
    
    def get_or_create_session(self, character_id: str, session_id: Optional[str] = None) -> ConversationSession:
        if session_id and session_id in self.sessions:
            session = self.sessions[session_id]
            session.last_activity = datetime.now()
            logger.info(f"📖 Retrieved existing session {session_id[:8]}... for {character_id}")
            return session
        
        new_session = ConversationSession(character_id, session_id)
        self.sessions[new_session.session_id] = new_session
        
        if character_id not in self.character_sessions:
            self.character_sessions[character_id] = []
        self.character_sessions[character_id].append(new_session.session_id)
        
        logger.info(f"🆕 Created new session {new_session.session_id[:8]}... for {character_id}")
        return new_session
    
    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        return self.sessions.get(session_id)
    
    def cleanup_expired_sessions(self, timeout_minutes: int = 30):
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if session.is_expired(timeout_minutes):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            session = self.sessions.pop(session_id, None)
            if session:
                character_sessions = self.character_sessions.get(session.character_id, [])
                if session_id in character_sessions:
                    character_sessions.remove(session_id)
                logger.info(f"🗑️ Cleaned up expired session {session_id[:8]}...")
        
        if expired_sessions:
            logger.info(f"🧹 Cleaned up {len(expired_sessions)} expired sessions")
    
    def get_character_sessions(self, character_id: str) -> List[ConversationSession]:
        session_ids = self.character_sessions.get(character_id, [])
        return [self.sessions[sid] for sid in session_ids if sid in self.sessions]
    
    def get_session_stats(self) -> Dict:
        active_sessions = len(self.sessions)
        character_counts = {char_id: len(sessions) for char_id, sessions in self.character_sessions.items()}
        
        return {
            "active_sessions": active_sessions,
            "sessions_by_character": character_counts,
            "total_conversations": sum(s.total_exchanges for s in self.sessions.values())
        }

_session_manager_instance: Optional[SessionManager] = None

def get_session_manager() -> SessionManager:
    global _session_manager_instance
    if _session_manager_instance is None:
        _session_manager_instance = SessionManager()
    return _session_manager_instance
