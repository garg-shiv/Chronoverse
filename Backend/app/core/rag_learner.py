import logging
from typing import Dict, List
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class RAGLearningSystem:
    def __init__(self):
        self.learning_threshold = 0.3
        self.specificity_threshold = 0.1
        logger.info("🧠 RAG Learning System initialized")
    
    def analyze_query_specificity(self, query: str) -> float:
        specific_keywords = [
            "when", "where", "how", "why", "what", "explain", "describe", "tell me about",
            "training", "weapon", "construction", "technique", "built", "made", "year",
            "battle", "siege", "design", "material", "process", "method"
        ]
        
        query_lower = query.lower()
        keyword_matches = sum(1 for keyword in specific_keywords if keyword in query_lower)
        
        word_count = len(query.split())
        specificity = min(keyword_matches * 0.3 + (word_count - 3) * 0.02, 1.0)
        
        return max(0, specificity)
    
    def assess_fact_relevance(self, retrieved_facts: List[Dict], query: str) -> float:
        if not retrieved_facts:
            return 0.0
        
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        
        total_relevance = 0
        for fact in retrieved_facts:
            fact_text = fact.get("text", "").lower()
            fact_words = set(re.findall(r'\b\w+\b', fact_text))
            
            word_overlap = len(query_words.intersection(fact_words))
            relevance = min(word_overlap / max(len(query_words), 1), 1.0)
            total_relevance += relevance
        
        return total_relevance / len(retrieved_facts)
    
    def evaluate_response_informativeness(self, response_text: str) -> float:
        if not response_text:
            return 0.0
        
        informative_patterns = [
            r'\d+',
            r'(century|year|BCE|CE|AD)',
            r'(technique|method|process|system)',
            r'(material|stone|metal|wood)',
            r'(built|constructed|designed|created)',
            r'(training|learning|practice)'
        ]
        
        pattern_matches = 0
        for pattern in informative_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                pattern_matches += 1
        
        length_factor = min(len(response_text) / 200, 1.0)
        informativeness = (pattern_matches * 0.1 + length_factor * 0.4)
        
        return min(informativeness, 1.0)
    
    def estimate_response_accuracy(self, response_text: str, retrieved_facts: List[Dict]) -> float:
        if not retrieved_facts:
            return 0.6
        
        response_lower = response_text.lower()
        accuracy_indicators = 0
        
        for fact in retrieved_facts:
            fact_text = fact.get("text", "").lower()
            fact_words = set(re.findall(r'\b\w{4,}\b', fact_text))
            
            word_overlap = sum(1 for word in fact_words if word in response_lower)
            if word_overlap > 0:
                accuracy_indicators += min(word_overlap / len(fact_words), 1.0)
        
        if retrieved_facts:
            accuracy = accuracy_indicators / len(retrieved_facts)
        else:
            accuracy = 0.6
        
        accuracy = max(0.4, min(accuracy + 0.3, 1.0))
        return accuracy
    
    async def analyze_and_learn_from_interaction(
        self, 
        character_id: str,
        user_query: str,
        retrieved_facts: List[Dict],
        llm_response: str
    ) -> Dict:
        
        logger.info(f"🔍 LEARNING DEBUG: Analyzing query: '{user_query[:50]}...'")
        logger.info(f"🔍 Retrieved facts count: {len(retrieved_facts)}")
        logger.info(f"🔍 Response length: {len(llm_response)} characters")
        
        quality_indicators = {
            'query_specificity': self.analyze_query_specificity(user_query),
            'fact_relevance': self.assess_fact_relevance(retrieved_facts, user_query),
            'response_informativeness': self.evaluate_response_informativeness(llm_response),
            'response_accuracy': self.estimate_response_accuracy(llm_response, retrieved_facts)
        }
        
        overall_score = (
            quality_indicators['query_specificity'] * 0.2 +
            quality_indicators['fact_relevance'] * 0.3 +
            quality_indicators['response_informativeness'] * 0.3 +
            quality_indicators['response_accuracy'] * 0.2
        )
        
        should_learn = (
            overall_score >= self.learning_threshold and 
            quality_indicators['query_specificity'] >= self.specificity_threshold
        )
        
        logger.info("🔍 QUALITY ASSESSMENT:")
        logger.info(f"   Overall Score: {overall_score:.3f}")
        logger.info(f"   Should Learn: {should_learn}")
        logger.info(f"   Indicators: {quality_indicators}")
        
        if should_learn:
            learning_reason = f"High quality interaction: Score {overall_score:.2f}"
            logger.info(f"✅ {learning_reason}")
        else:
            learning_reason = f"Score: {overall_score:.2f}, Specificity: {quality_indicators['query_specificity']:.2f}"
            logger.info(f"   Reason: {learning_reason}")
            logger.info(f"❌ Quality threshold not met: {learning_reason}")
        
        return {
            'learned': should_learn,
            'overall_score': overall_score,
            'quality_indicators': quality_indicators,
            'learning_reason': learning_reason,
            'character_id': character_id,
            'timestamp': datetime.now().isoformat()
        }

_rag_learner_instance = None

async def get_rag_learner():
    global _rag_learner_instance
    if _rag_learner_instance is None:
        _rag_learner_instance = RAGLearningSystem()
    return _rag_learner_instance
