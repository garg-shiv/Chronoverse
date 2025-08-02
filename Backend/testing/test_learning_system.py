import requests
import time

def test_learning_system():
    base_url = "http://localhost:8000"
    
    # Test queries that should trigger learning
    learning_queries = [
        {
            "character_id": "roman_gladiator",
            "user_text": "What specific techniques did gladiators use to disarm opponents with nets and tridents?"
        },
        {
            "character_id": "mughal_architect", 
            "user_text": "How did you calculate the precise mathematical ratios for the Taj Mahal's garden layout?"
        }
    ]
    
    print("🎓 Testing RAG Learning System")
    print("=" * 50)
    
    for query in learning_queries:
        print(f"\n🔍 Testing: {query['user_text'][:50]}...")
        
        # Send dialogue request
        response = requests.post(f"{base_url}/api/v1/dialogue", data=query)
        
        if response.status_code == 200:
            print("✅ Dialogue successful")
            
            # Check learning stats
            time.sleep(1)
            stats_response = requests.get(f"{base_url}/api/v1/learning/stats")
            
            if stats_response.status_code == 200:
                stats = stats_response.json()
                if stats["success"]:
                    learned_facts = stats["stats"]["total_learned_facts"]
                    print(f"📈 Total learned facts: {learned_facts}")
                    
    print("\n🎉 Learning system test complete!")

if __name__ == "__main__":
    test_learning_system()
