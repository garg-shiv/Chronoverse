import asyncio
import logging
import sys
import os
from pathlib import Path
from typing import Dict

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[2]
sys.path.append(str(root))

from app.core.rag import get_rag_service
from app.data.enhanced_historical_facts import ENHANCED_HISTORICAL_FACTS, get_character_facts

logger = logging.getLogger(__name__)

class EnhancedKnowledgeSeeder:
    
    def __init__(self):
        self.rag_service = None
        self.seeding_stats = {}
    
    async def initialize_complete_knowledge_base(self):
        logger.info("🚀 Starting Enhanced Chronoverse Knowledge Base Initialization")
        logger.info("=" * 80)
        
        try:
            self.rag_service = get_rag_service()
            total_facts_loaded = 0
            
            for character_id in ENHANCED_HISTORICAL_FACTS.keys():
                logger.info(f"\n📚 Processing {character_id}...")
                
                character_data = get_character_facts(character_id)
                if not character_data:
                    logger.warning(f"⚠️ No data found for {character_id}")
                    continue
                
                char_info = character_data.get("character_info", {})
                logger.info(f"👤 {char_info.get('name', 'Unknown')}")
                logger.info(f"📅 Period: {char_info.get('period', 'Unknown')}")
                
                facts = character_data.get("facts", [])
                logger.info(f"📊 Processing {len(facts)} enhanced facts...")
                
                success = self.rag_service.add_knowledge(character_id, facts)
                
                if success:
                    categories = {}
                    for fact in facts:
                        category = fact.get("category", "general")
                        categories[category] = categories.get(category, 0) + 1
                    
                    logger.info(f"✅ Successfully loaded {len(facts)} facts for {character_id}")
                    logger.info(f"📈 Categories: {dict(categories)}")
                    
                    self.seeding_stats[character_id] = {
                        "total_facts": len(facts),
                        "categories": categories,
                        "status": "success"
                    }
                    total_facts_loaded += len(facts)
                else:
                    logger.error(f"❌ Failed to load facts for {character_id}")
                    self.seeding_stats[character_id] = {
                        "total_facts": 0,
                        "categories": {},
                        "status": "failed"
                    }
            
            logger.info("\n" + "=" * 80)
            logger.info("🎉 Enhanced Knowledge Base Initialization Complete!")
            logger.info(f"📊 Total Facts Loaded: {total_facts_loaded}")
            
            return self.seeding_stats
            
        except Exception as e:
            logger.error(f"❌ Knowledge base initialization failed: {e}")
            raise
    
    async def validate_knowledge_base(self):
        logger.info("\n🔍 Validating Knowledge Base...")
        
        validation_results = {}
        test_queries = ["training", "construction", "writing", "combat", "daily life"]
        
        for character_id in ENHANCED_HISTORICAL_FACTS.keys():
            logger.info(f"Validating {character_id}...")
            
            character_results = {}
            for query in test_queries:
                try:
                    facts = await self.rag_service.retrieve_relevant_facts(
                        character_id=character_id,
                        query=query,
                        max_results=3
                    )
                    character_results[query] = len(facts)
                except Exception as e:
                    character_results[query] = f"Error: {e}"
            
            validation_results[character_id] = character_results
            successful_queries = sum(1 for v in character_results.values() if isinstance(v, int) and v > 0)
            logger.info(f"✅ {character_id}: {successful_queries}/{len(test_queries)} queries successful")
        
        return validation_results

async def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
    
    seeder = EnhancedKnowledgeSeeder()
    
    try:
        stats = await seeder.initialize_complete_knowledge_base()
        validation = await seeder.validate_knowledge_base()
        
        logger.info("\n🎉 Enhanced Knowledge Base Setup Complete!")
        logger.info("Your historical characters now have comprehensive knowledge!")
        
        return stats, validation
        
    except Exception as e:
        logger.error(f"❌ Knowledge seeding failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
