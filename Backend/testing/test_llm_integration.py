import requests
import json

def test_llm_integration():
    base_url = "http://localhost:8000"
    
    test_cases = [
        {
            "character_id": "roman_gladiator",
            "question": "What was your most dangerous fight in the arena?",
        },
        {
            "character_id": "mughal_architect", 
            "question": "How did you design the Taj Mahal's dome?",
        },
        {
            "character_id": "egyptian_scribe",
            "question": "Why was writing sacred in ancient Egypt?",
        }
    ]
    
    print("🧠 Testing Enhanced AI Historical Characters")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. Testing {test['character_id']}")
        print(f"   Question: '{test['question']}'")
        
        try:
            data = {
                "character_id": test["character_id"],
                "user_text": test["question"],
                "scene_context": "general"
            }
            
            response = requests.post(f"{base_url}/api/v1/dialogue", data=data)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result["response_text"]
                
                print(f"   ✅ Response generated ({len(response_text)} characters)")
                print(f"   📝 Response: \"{response_text}\"")
                print(f"   ⏱️ Processing time: {result['processing_time_ms']}ms")
                
                personal_indicators = ["I", "my", "we", "our", "me"]
                if any(word in response_text for word in personal_indicators):
                    print(f"   🎭 ✅ Response appears to be in first person (good character voice)")
                else:
                    print(f"   ⚠️ Response might not be fully in character")
                    
            else:
                print(f"   ❌ Request failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
    
    print(f"\n🎉 LLM integration testing complete!")

if __name__ == "__main__":
    test_llm_integration()
