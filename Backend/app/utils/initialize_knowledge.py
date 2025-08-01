import sys
import os
import asyncio
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.rag import get_rag_service
from data.historical_facts import HISTORICAL_KNOWLEDGE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def initialize_knowledge_base():
    logger.info("🚀 Initializing Chronoverse Knowledge Base...")
    
    try:
        rag_service = get_rag_service()
        
        for character_id, facts in HISTORICAL_KNOWLEDGE.items():
            logger.info(f"📚 Loading knowledge for {character_id}...")
            
            success = rag_service.add_knowledge(character_id, facts)
            if success:
                stats = rag_service.get_collection_stats(character_id)
                logger.info(f"✅ {character_id}: {stats['total_facts']} facts loaded")
            else:
                logger.error(f"❌ Failed to load knowledge for {character_id}")
        
        logger.info("🎉 Knowledge base initialization complete!")
        
        await test_knowledge_retrieval(rag_service)
        
    except Exception as e:
        logger.error(f"❌ Knowledge base initialization failed: {e}")

async def test_knowledge_retrieval(rag_service):
    logger.info("🧪 Testing knowledge retrieval...")
    
    test_queries = [
        ("roman_gladiator", "How did gladiators train?"),
        ("mughal_architect", "What materials were used in the Taj Mahal?"),
        ("egyptian_scribe", "What did scribes write on?")
    ]
    
    for character_id, query in test_queries:
        logger.info(f"🔍 Testing: '{query}' for {character_id}")
        facts = await rag_service.retrieve_relevant_facts(character_id, query, max_results=2)
        
        if facts:
            logger.info(f"✅ Retrieved {len(facts)} relevant facts")
            logger.info(f"    Top result: {facts[0]['text'][:100]}...")
        else:
            logger.warning(f"⚠️ No facts retrieved for query")

if __name__ == "__main__":
    asyncio.run(initialize_knowledge_base())