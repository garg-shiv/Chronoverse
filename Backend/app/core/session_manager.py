from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid
import logging

logger = logging.getLogger(__name__)

class ConversationSession:
    def __init__(self, session_id: str, character_id: str):
        self.session_id = session_id
        self.character_id = character_id
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.conversation_history: List[Dict] = []
        self.context_summary = ""

    def add_exchange(self, user_input: str, character_response: str):
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "character": character_response,
            "exchange_id": len(self.conversation_history) + 1
        }
        
        self.conversation_history.append(exchange)
        self.last_activity = datetime.now()
        
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]

    def get_recent_context(self, max_exchanges: int = 3) -> List[Dict]:
        return self.conversation_history[-max_exchanges:] if self.conversation_history else []

    def is_expired(self, timeout_minutes: int = 30) -> bool:
        return datetime.now() - self.last_activity > timedelta(minutes=timeout_minutes)

class SessionManager:
    def __init__(self):
        self.active_sessions: Dict[str, ConversationSession] = {}
        self.cleanup_interval = 60

    def get_or_create_session(self, character_id: str, session_id: Optional[str] = None) -> ConversationSession:
        if session_id and session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            if not session.is_expired():
                return session
            else:
                del self.active_sessions[session_id]
        
        new_session_id = session_id or str(uuid.uuid4())
        new_session = ConversationSession(new_session_id, character_id)
        self.active_sessions[new_session_id] = new_session
        
        logger.info(f"🆕 Created new session {new_session_id} for {character_id}")
        return new_session

    def cleanup_expired_sessions(self):
        expired_sessions = [
            session_id for session_id, session in self.active_sessions.items()
            if session.is_expired()
        ]
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
            logger.info(f"🧹 Cleaned up expired session {session_id}")

    def get_session_stats(self) -> Dict:
        return {
            "active_sessions": len(self.active_sessions),
            "total_exchanges": sum(len(s.conversation_history) for s in self.active_sessions.values()),
            "characters_in_use": list(set(s.character_id for s in self.active_sessions.values()))
        }

_session_manager: Optional[SessionManager] = None

def get_session_manager() -> SessionManager:
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager