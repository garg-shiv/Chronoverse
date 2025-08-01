import ollama
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class HistoricalCharacterLLM:
    
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.model_name = model_name
        self.client = ollama.Client(host='http://127.0.0.1:12345')
        self.character_personas = self._load_character_personas()
        logger.info(f"🧠 Initializing Historical Character LLM with model: {model_name}")
        self._verify_model()
    
    def _verify_model(self):
        try:
            logger.info("🔍 Connecting to Ollama at 127.0.0.1:12345")
            models = self.client.list()
            
            if 'models' in models:
                available_models = []
                for model in models['models']:
                    if 'name' in model:
                        available_models.append(model['name'])
                    elif 'model' in model:
                        available_models.append(model['model'])
                    elif isinstance(model, str):
                        available_models.append(model)
            else:
                available_models = [str(model) for model in models if model]
            
            logger.info(f"📋 Available models: {available_models}")
            
            if self.model_name in available_models:
                logger.info(f"✅ LLM model {self.model_name} is ready")
            else:
                logger.warning(f"⚠️ Model {self.model_name} not found. Available: {available_models}")
                logger.info("🔄 Attempting to continue anyway...")
                
        except Exception as e:
            logger.error(f"❌ Failed to verify Ollama model: {e}")
            logger.info("🔄 Continuing without model verification...")
    
    def _load_character_personas(self) -> Dict[str, Dict]:
        return {
            "roman_gladiator": {
                "name": "Marcus Quintus",
                "role": "Veteran gladiator of the Colosseum",
                "personality": "Confident, battle-hardened, speaks with authority about combat and honor",
                "speech_style": "Direct, uses military terminology, occasional Latin phrases like 'Salve'",
                "background": "Fought for 8 years in the arena, trained hundreds of novices at the ludus",
                "expertise": ["combat techniques", "arena politics", "gladiator training", "Roman society"],
                "greeting_style": "Addresses people as 'citizen' or 'friend', references personal combat experiences"
            },
            "mughal_architect": {
                "name": "Ustad Ahmad Lahauri",
                "role": "Master architect of the Taj Mahal",
                "personality": "Wise, artistic, deeply spiritual, speaks of divine inspiration in architecture",
                "speech_style": "Eloquent, uses metaphors of light and geometry, references Islamic art principles",
                "background": "Chief architect under Shah Jahan, designed multiple imperial monuments",
                "expertise": ["Islamic architecture", "mathematical proportions", "construction techniques", "Mughal court life"],
                "greeting_style": "Begins with 'Peace be upon you', speaks of architecture as divine art"
            },
            "egyptian_scribe": {
                "name": "Khaemwaset",
                "role": "Royal scribe in the House of Life",
                "personality": "Learned, formal, devoted to preserving knowledge and serving the gods",
                "speech_style": "Formal, references Egyptian deities like Thoth, uses scribal terminology",
                "background": "Served three pharaohs, keeper of sacred texts and royal records",
                "expertise": ["hieroglyphic writing", "religious ceremonies", "Egyptian mathematics", "afterlife beliefs"],
                "greeting_style": "Formal address, references serving Pharaoh and the gods"
            }
        }
    
    async def generate_response(
        self, 
        character_id: str, 
        user_query: str, 
        historical_facts: List[Dict], 
        conversation_history: List[Dict] = None
    ) -> Dict[str, str]:
        
        if character_id not in self.character_personas:
            raise ValueError(f"Unknown character: {character_id}")
        
        try:
            prompt = self._build_character_prompt(
                character_id, user_query, historical_facts, conversation_history
            )
            
            logger.info(f"🎭 Generating response for {character_id}: '{user_query[:50]}...'")
            
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.7,
                    'max_tokens': 150,
                    'num_predict': 150,
                    'top_p': 0.9,
                    'stop': ['\n\nUser:', '\n\nHuman:', '\n\nQ:']
                }
            )
            
            response_text = response['response'].strip()
            response_text = self._clean_response(response_text, character_id)
            
            logger.info(f"✅ Generated {len(response_text)} character response")
            
            return {
                "response_text": response_text,
                "character_id": character_id,
                "model_used": self.model_name,
                "historical_facts_used": len(historical_facts),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ LLM generation failed for {character_id}: {e}")
            
            fallback_response = self._generate_fallback_response(
                character_id, user_query, historical_facts
            )
            
            return {
                "response_text": fallback_response,
                "character_id": character_id,
                "model_used": "fallback_template",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def generate_simple_response(
        self, 
        character_id: str, 
        user_query: str
    ) -> Dict[str, str]:
        
        if character_id not in self.character_personas:
            raise ValueError(f"Unknown character: {character_id}")
        
        try:
            prompt = self._build_simple_prompt(character_id, user_query)
            
            logger.info(f"💬 Generating simple response for {character_id}")
            
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.8,
                    'max_tokens': 100,
                    'num_predict': 100,
                    'top_p': 0.9
                }
            )
            
            response_text = response['response'].strip()
            response_text = self._clean_response(response_text, character_id)
            
            logger.info(f"✅ Generated simple response: {len(response_text)} chars")
            
            return {
                "response_text": response_text,
                "character_id": character_id,
                "model_used": self.model_name,
                "response_type": "conversational",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Simple response generation failed: {e}")
            
            persona = self.character_personas[character_id]
            fallback = f"Greetings! I am {persona['name']}, {persona['role']}. How may I assist you today?"
            
            return {
                "response_text": fallback,
                "character_id": character_id,
                "model_used": "fallback_simple",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _build_character_prompt(
        self, 
        character_id: str, 
        user_query: str, 
        historical_facts: List[Dict], 
        conversation_history: List[Dict] = None
    ) -> str:
        
        persona = self.character_personas[character_id]
        
        facts_context = "\n".join([
            f"- {fact['text']}" for fact in historical_facts[:3]
        ]) if historical_facts else "Use your general historical knowledge."
        
        history_context = ""
        if conversation_history:
            recent_history = conversation_history[-2:]
            for exchange in recent_history:
                history_context += f"User: {exchange.get('user', '')}\nYou: {exchange.get('character', '')}\n"
        
        prompt = f"""You are {persona['name']}, a {persona['role']} in ancient times.

CHARACTER BACKGROUND:
- Personality: {persona['personality']}
- Speech Style: {persona['speech_style']}
- Background: {persona['background']}

HISTORICAL CONTEXT (use this information):
{facts_context}

{history_context if history_context else ""}

USER: "{user_query}"

INSTRUCTIONS:
1. Respond as {persona['name']} in character
2. Use historical context provided
3. Keep response 2-3 sentences
4. Reference personal experience
5. Be engaging

{persona['name']}:"""

        return prompt
    
    def _build_simple_prompt(self, character_id: str, user_query: str) -> str:
        persona = self.character_personas[character_id]
        
        prompt = f"""You are {persona['name']}, a {persona['role']}.

Personality: {persona['personality']}
Speech Style: {persona['speech_style']}

USER: "{user_query}"

Respond as {persona['name']} with a friendly, brief response (1-2 sentences):

{persona['name']}:"""

        return prompt
    
    def _clean_response(self, response_text: str, character_id: str) -> str:
        persona = self.character_personas[character_id]
        
        prefixes_to_remove = [
            f"{persona['name']} responds:",
            f"{persona['name']}:",
            f"Response as {persona['name']}:",
            "I respond:",
            "Response:",
        ]
        
        for prefix in prefixes_to_remove:
            if response_text.startswith(prefix):
                response_text = response_text[len(prefix):].strip()
        
        return response_text
    
    def _generate_fallback_response(
        self, 
        character_id: str, 
        user_query: str, 
        historical_facts: List[Dict]
    ) -> str:
        
        persona = self.character_personas[character_id]
        
        if historical_facts:
            fact = historical_facts[0]['text']
            return f"As {persona['name']}, I can tell you that {fact.lower()} What would you like to know more about?"
        else:
            return f"Greetings! I am {persona['name']}, {persona['role']}. I'd be happy to share my knowledge with you."
    
    def get_model_info(self) -> Dict[str, str]:
        return {
            "model_name": self.model_name,
            "host": "127.0.0.1:12345",
            "characters_available": len(self.character_personas),
            "status": "ready" if self.client else "unavailable",
            "features": ["rag_enhanced", "conversational", "adaptive_routing"]
        }

_llm_instance: Optional[HistoricalCharacterLLM] = None

def get_llm_service() -> HistoricalCharacterLLM:
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = HistoricalCharacterLLM()
    return _llm_instance
