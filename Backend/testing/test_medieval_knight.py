import requests

def test_sir_gareth():
    base_url = "http://localhost:8000/api/v1/dialogue"
    
    knight_tests = [
        "Tell me about your training as a knight",
        "What is the Code of Chivalry?", 
        "Describe a medieval castle siege",
        "How heavy was your armor in battle?"
    ]
    
    print("⚔️ Testing Sir Gareth the Medieval Knight")
    print("=" * 50)
    
    for i, query in enumerate(knight_tests, 1):
        print(f"\n{i}. Testing: '{query}'")
        
        response = requests.post(base_url, data={
            "character_id": "medieval_knight",
            "user_text": query
        })
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Sir Gareth: '{result['response_text'][:100]}...'")
            if result.get('audio_url'):
                print(f"   🎵 Voice: {result['audio_url']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")

if __name__ == "__main__":
    test_sir_gareth()
