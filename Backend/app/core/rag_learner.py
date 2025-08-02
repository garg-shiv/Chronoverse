import asyncio
import logging
import hashlib
from typing import Dict, List, Optional
from datetime import datetime
from app.core.rag import get_rag_service

logger = logging.getLogger(__name__)

class RAGLearningSystem:
    def __init__(self):
        self.rag_service = None
        self.learning_stats = {}
        self.query_cache = {}

    async def initialize(self):
        self.rag_service = get_rag_service()
        logger.info("🧠 RAG Learning System initialized")

    async def analyze_and_learn_from_interaction(
        self,
        character_id: str,
        user_query: str,
        retrieved_facts: List[Dict],
        llm_response: str,
        response_quality_score: float = None
    ) -> Dict:
        try:
            logger.info(f"🔍 LEARNING DEBUG: Analyzing query: '{user_query[:50]}...'")
            logger.info(f"🔍 Retrieved facts count: {len(retrieved_facts)}")
            logger.info(f"🔍 Response length: {len(llm_response)} characters")
            
            quality_assessment = await self._assess_interaction_quality(
                user_query, retrieved_facts, llm_response, response_quality_score
            )
            
            logger.info(f"🔍 QUALITY ASSESSMENT:")
            logger.info(f"   Overall Score: {quality_assessment['overall_score']:.3f}")
            logger.info(f"   Should Learn: {quality_assessment['should_learn']}")
            logger.info(f"   Indicators: {quality_assessment['indicators']}")
            logger.info(f"   Reason: {quality_assessment['reason']}")
            
            if quality_assessment["should_learn"]:
                logger.info("✅ Quality threshold met - attempting to learn")
                
                new_knowledge = await self._extract_knowledge_from_interaction(
                    character_id, user_query, llm_response, quality_assessment
                )
                
                if new_knowledge:
                    logger.info(f"📝 Generated new knowledge: {new_knowledge['category']}")
                    logger.info(f"📝 Text preview: {new_knowledge['text'][:100]}...")
                    
                    success = await self._add_learned_knowledge(character_id, new_knowledge)
                    
                    if success:
                        logger.info(f"🎓 Successfully learned from: '{user_query[:50]}...'")
                        return {"learned": True, "knowledge": new_knowledge}
                    else:
                        logger.error(f"❌ Failed to add knowledge to RAG system")
                        return {"learned": False, "reason": "RAG addition failed"}
                else:
                    logger.warning(f"⚠️ Could not extract knowledge from interaction")
                    return {"learned": False, "reason": "Knowledge extraction failed"}
            else:
                logger.info(f"❌ Quality threshold not met: {quality_assessment['reason']}")
                return {"learned": False, "reason": quality_assessment.get("reason", "Quality threshold not met")}
        
        except Exception as e:
            logger.error(f"❌ Learning analysis failed: {e}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            return {"learned": False, "error": str(e)}

    async def _assess_interaction_quality(
        self, 
        user_query: str, 
        retrieved_facts: List[Dict], 
        llm_response: str, 
        response_quality_score: float = None
    ) -> Dict:
        quality_indicators = {
            "query_specificity": self._assess_query_specificity(user_query),
            "fact_relevance": self._assess_fact_relevance(retrieved_facts, user_query),
            "response_informativeness": self._assess_response_informativeness(llm_response),
            "response_accuracy": response_quality_score or self._estimate_response_accuracy(llm_response)
        }
        
        weights = {
            "query_specificity": 0.3,
            "fact_relevance": 0.25,
            "response_informativeness": 0.25,
            "response_accuracy": 0.2
        }
        
        overall_score = sum(
            quality_indicators[key] * weights[key] 
            for key in weights.keys()
        )
        
        should_learn = overall_score > 0.3 and quality_indicators["query_specificity"] > 0.2
        
        return {
            "should_learn": should_learn,
            "overall_score": overall_score,
            "indicators": quality_indicators,
            "reason": f"Score: {overall_score:.2f}, Specificity: {quality_indicators['query_specificity']:.2f}"
        }

    def _assess_query_specificity(self, query: str) -> float:
        specific_indicators = [
            "how", "why", "when", "where", "what", "which", "describe", "explain",
            "technique", "method", "process", "construction", "training", "weapon",
            "material", "design", "ceremony", "ritual", "battle", "combat"
        ]
        
        query_lower = query.lower()
        specificity_score = sum(0.1 for indicator in specific_indicators if indicator in query_lower)
        
        if len(query.split()) < 4:
            specificity_score *= 0.5
        
        if len(query.split()) > 8:
            specificity_score *= 1.2
            
        return min(specificity_score, 1.0)

    def _assess_fact_relevance(self, retrieved_facts: List[Dict], query: str) -> float:
        if not retrieved_facts:
            return 0.0
        
        avg_relevance = sum(fact.get("relevance_score", 0.5) for fact in retrieved_facts) / len(retrieved_facts)
        
        categories = set(fact.get("category", "general") for fact in retrieved_facts)
        category_diversity = len(categories) / max(len(retrieved_facts), 1)
        
        return (avg_relevance * 0.7) + (category_diversity * 0.3)

    def _assess_response_informativeness(self, response: str) -> float:
        word_count = len(response.split())
        length_score = min(word_count / 50, 1.0)
        
        quality_indicators = [
            "specific", "detail", "technique", "method", "because", "reason",
            "example", "instance", "during", "period", "century", "ancient"
        ]
        
        content_score = sum(0.1 for indicator in quality_indicators if indicator in response.lower())
        content_score = min(content_score, 1.0)
        
        personal_indicators = ["I", "my", "we", "our", "myself"]
        personal_score = min(sum(0.1 for indicator in personal_indicators if indicator in response), 0.3)
        
        return (length_score * 0.4) + (content_score * 0.4) + (personal_score * 0.2)

    def _estimate_response_accuracy(self, response: str) -> float:
        confidence_indicators = ["precisely", "exactly", "specifically", "according to", "documented"]
        uncertainty_indicators = ["might", "perhaps", "possibly", "unclear", "uncertain"]
        
        response_lower = response.lower()
        confidence_score = sum(0.1 for indicator in confidence_indicators if indicator in response_lower)
        uncertainty_penalty = sum(0.1 for indicator in uncertainty_indicators if indicator in response_lower)
        
        base_score = 0.7
        final_score = base_score + confidence_score - uncertainty_penalty
        
        return max(0.0, min(final_score, 1.0))

    async def _extract_knowledge_from_interaction(
        self,
        character_id: str,
        user_query: str,
        llm_response: str,
        quality_assessment: Dict
    ) -> Optional[Dict]:
        try:
            query_hash = hashlib.md5(user_query.encode()).hexdigest()[:8]
            category = self._categorize_query(user_query)
            
            new_fact = {
                "text": f"User inquiry: {user_query}. Response: {llm_response[:200]}...",
                "category": category,
                "subcategory": "user_interaction",
                "historical_accuracy": "user_generated",
                "source": f"Interactive learning session {datetime.now().strftime('%Y-%m-%d')}",
                "interaction_quality": quality_assessment["overall_score"],
                "query_hash": query_hash,
                "learned_date": datetime.now().isoformat()
            }
            
            return new_fact
            
        except Exception as e:
            logger.error(f"❌ Knowledge extraction failed: {e}")
            return None

    def _categorize_query(self, query: str) -> str:
        category_keywords = {
            "combat_techniques": ["fight", "combat", "battle", "weapon", "sword", "stance", "technique"],
            "training": ["train", "practice", "learn", "preparation", "exercise", "drill"],
            "construction": ["build", "construct", "material", "stone", "marble", "foundation"],
            "architecture": ["design", "structure", "dome", "minaret", "proportion", "geometry"],
            "writing_systems": ["write", "script", "hieroglyph", "symbol", "text", "document"],
            "daily_life": ["daily", "life", "food", "living", "routine", "society"],
            "religion": ["god", "deity", "prayer", "ritual", "ceremony", "sacred"],
            "tools": ["tool", "equipment", "instrument", "implement"]
        }
        
        query_lower = query.lower()
        
        for category, keywords in category_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return category
        
        return "general"

    async def _add_learned_knowledge(self, character_id: str, new_fact: Dict) -> bool:
        try:
            success = self.rag_service.add_knowledge(character_id, [new_fact])
            
            if success:
                if character_id not in self.learning_stats:
                    self.learning_stats[character_id] = {"learned_facts": 0, "categories": {}}
                
                self.learning_stats[character_id]["learned_facts"] += 1
                
                category = new_fact.get("category", "general")
                if category not in self.learning_stats[character_id]["categories"]:
                    self.learning_stats[character_id]["categories"][category] = 0
                self.learning_stats[character_id]["categories"][category] += 1
                
                logger.info(f"📈 Added learned fact to {character_id}: {new_fact['category']}")
                return True
                
        except Exception as e:
            logger.error(f"❌ Failed to add learned knowledge: {e}")
            
        return False

    def get_learning_statistics(self) -> Dict:
        return {
            "learning_stats": self.learning_stats,
            "total_learned_facts": sum(stats["learned_facts"] for stats in self.learning_stats.values()),
            "characters_learning": len(self.learning_stats),
            "timestamp": datetime.now().isoformat()
        }

_rag_learner_instance: Optional[RAGLearningSystem] = None

async def get_rag_learner() -> RAGLearningSystem:
    global _rag_learner_instance
    if _rag_learner_instance is None:
        _rag_learner_instance = RAGLearningSystem()
        await _rag_learner_instance.initialize()
    return _rag_learner_instance