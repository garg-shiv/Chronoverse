import requests
import time

def test_conversation_memory():
    base_url = "http://localhost:8000/api/v1/dialogue"
    
    # Test conversation with memory
    session_id = None
    
    conversation = [
        "Tell me about gladiator training with wooden swords",
        "How long did that training take?",
        "What happened after the training you mentioned?",
        "Thank you for explaining the training process"
    ]
    
    print("🧠 Testing Conversation Memory System")
    print("=" * 60)
    
    for i, query in enumerate(conversation, 1):
        print(f"\n{i}. User: '{query}'")
        
        data = {
            "character_id": "roman_gladiator",
            "user_text": query
        }
        
        if session_id:
            data["session_id"] = session_id
        
        response = requests.post(base_url, data=data)
        
        if response.status_code == 200:
            result = response.json()
            session_id = result.get("session_id")  # Store session ID
            
            print(f"   Marcus: '{result['response_text'][:100]}...'")
            print(f"   Session: {session_id}")
            print(f"   Time: {result['processing_time_ms']}ms")
            
            if i > 1:  # Check for memory references after first exchange
                response_text = result['response_text'].lower()
                memory_indicators = ['that', 'the training', 'i mentioned', 'as i said', 'the process']
                found_memory = any(indicator in response_text for indicator in memory_indicators)
                
                if found_memory:
                    print(f"   ✅ Memory reference detected!")
                else:
                    print(f"   ⚠️ No clear memory reference found")
        else:
            print(f"   ❌ Error: {response.status_code}")
        
        time.sleep(1)  # Brief pause between messages
    
    print(f"\n🎉 Memory system testing complete!")

if __name__ == "__main__":
    test_conversation_memory()
