import logging
import asyncio
from app.data.enhanced_historical_facts import HISTORICAL_FACTS
from app.core.rag import get_rag_service

logger = logging.getLogger(__name__)

async def seed_knowledge_base():
    """
    Seed the knowledge base with historical facts for all characters
    """
    try:
        logger.info("🌱 Starting knowledge base seeding...")
        
        rag_service = get_rag_service()
        
        characters = [
            "roman_gladiator", 
            "mughal_architect", 
            "egyptian_scribe", 
            "medieval_knight", 
            "viking_explorer", 
            "renaissance_master"
        ]
        
        total_facts_seeded = 0
        successful_characters = []
        failed_characters = []
        
        for character_id in characters:
            if character_id in HISTORICAL_FACTS:
                character_data = HISTORICAL_FACTS[character_id]
                facts_list = character_data["facts"]
                character_name = character_data["character_info"]["name"]
                
                logger.info(f"🏛️ Seeding {len(facts_list)} facts for {character_name} ({character_id})")
                
                try:
                    # Convert facts to the format expected by add_knowledge
                    formatted_facts = []
                    for fact in facts_list:
                        formatted_fact = {
                            "text": fact["text"],
                            "category": fact["category"],
                            "source": fact.get("source", "Historical records"),
                            "accuracy": fact.get("historical_accuracy", "high")
                        }
                        formatted_facts.append(formatted_fact)
                    
                    # Call add_knowledge WITHOUT await (it's synchronous)
                    result = rag_service.add_knowledge(character_id, formatted_facts)
                    
                    total_facts_seeded += len(formatted_facts)
                    successful_characters.append(character_id)
                    logger.info(f"✅ Successfully seeded {len(formatted_facts)} facts for {character_name}")
                    
                except Exception as character_error:
                    failed_characters.append(character_id)
                    logger.error(f"❌ Failed to seed {character_name}: {character_error}")
                    continue
            else:
                failed_characters.append(character_id)
                logger.error(f"❌ Unknown character: {character_id}")
        
        logger.info(f"🎉 Knowledge base seeding complete!")
        logger.info(f"📊 Summary: {len(successful_characters)} successful, {len(failed_characters)} failed")
        logger.info(f"📚 Total facts seeded: {total_facts_seeded}")
        
        # Verification
        logger.info("🔍 Verifying seeded knowledge...")
        for character_id in successful_characters:
            try:
                # retrieve_relevant_facts might be async, so keep await here
                test_facts = await rag_service.retrieve_relevant_facts(
                    character_id=character_id,
                    query="test",
                    max_results=5
                )
                character_name = HISTORICAL_FACTS[character_id]["character_info"]["name"]
                logger.info(f"📋 {character_name}: {len(test_facts)} facts verified")
            except Exception as e:
                logger.warning(f"⚠️ Could not verify {character_id}: {e}")
        
        return {
            "success": len(successful_characters) > 0,
            "characters_seeded": len(successful_characters),
            "characters_failed": len(failed_characters),
            "total_facts": total_facts_seeded,
            "successful_characters": successful_characters,
            "failed_characters": failed_characters
        }
        
    except Exception as e:
        logger.error(f"❌ Critical knowledge seeding failure: {e}")
        return {
            "success": False,
            "error": str(e),
            "characters_seeded": 0,
            "total_facts": 0
        }

def main():
    """
    Main entry point for knowledge seeding
    """
    print("🚀 Chronoverse Knowledge Base Seeder")
    print("=" * 50)
    
    # Check data integrity
    print("🔍 Checking HISTORICAL_FACTS structure...")
    try:
        print(f"✅ Found {len(HISTORICAL_FACTS)} characters")
        for char_id, data in HISTORICAL_FACTS.items():
            fact_count = len(data["facts"]) if "facts" in data else 0
            char_name = data.get("character_info", {}).get("name", char_id)
            print(f"   {char_name}: {fact_count} facts")
    except Exception as e:
        print(f"❌ Error checking data: {e}")
        return
    
    # Run seeding
    result = asyncio.run(seed_knowledge_base())
    
    print("\n📋 SEEDING RESULTS:")
    print(f"   Success: {result.get('success', False)}")
    print(f"   Characters Seeded: {result.get('characters_seeded', 0)}")
    print(f"   Total Facts: {result.get('total_facts', 0)}")
    
    if result.get('successful_characters'):
        print(f"   ✅ Successful: {result['successful_characters']}")
    
    if result.get('failed_characters'):
        print(f"   ❌ Failed: {result['failed_characters']}")
    
    print("\n🎉 Knowledge seeding process complete!")

if __name__ == "__main__":
    main()
