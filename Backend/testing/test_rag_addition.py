# Create Backend/test_rag_addition.py
import asyncio
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]  # Go up to backend directory
sys.path.append(str(root))

from app.core.rag import get_rag_service

async def test_rag_addition():
    """Test if we can add knowledge to RAG directly"""
    
    rag_service = get_rag_service()
    
    test_fact = {
        "text": "TEST: This is a test fact to verify RAG learning works.",
        "category": "test",
        "subcategory": "debug",
        "historical_accuracy": "test",
        "source": "debugging session"
    }
    
    print("🧪 Testing direct RAG addition...")
    success = rag_service.add_knowledge("roman_gladiator", [test_fact])
    
    if success:
        print("✅ Direct RAG addition successful")
        
        # Try to retrieve it
        facts = await rag_service.retrieve_relevant_facts(
            character_id="roman_gladiator",
            query="test fact debug",
            max_results=1
        )
        
        if facts:
            print(f"✅ Retrieved test fact: {facts[0]['text'][:50]}...")
        else:
            print("❌ Could not retrieve test fact")
    else:
        print("❌ Direct RAG addition failed")

if __name__ == "__main__":
    asyncio.run(test_rag_addition())
