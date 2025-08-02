import requests
import json
import time

def test_enhanced_chronoverse():
    base_url = "http://localhost:8000/api/v1/dialogue"
    
    test_cases = [
        {
            "name": "Gladiator Combat Stances",
            "data": {
                "character_id": "roman_gladiator",
                "user_text": "What were the four fundamental fighting stances?"
            },
            "expected_keywords": ["prima", "secunda", "tertia", "quarta", "combat", "stances"]
        },
        {
            "name": "Taj Mahal Dome Construction", 
            "data": {
                "character_id": "mughal_architect",
                "user_text": "How did you construct the double-shell dome?"
            },
            "expected_keywords": ["double-shell", "inner dome", "outer dome", "construction"]
        },
        {
            "name": "Hieroglyphic Writing System",
            "data": {
                "character_id": "egyptian_scribe", 
                "user_text": "Explain the 700 hieroglyphic signs and their functions"
            },
            "expected_keywords": ["700", "signs", "logograms", "phonograms", "determinatives"]
        },
        {
            "name": "Quick Conversational Test",
            "data": {
                "character_id": "roman_gladiator",
                "user_text": "Hello, nice to meet you"
            },
            "expected_keywords": ["salve", "marcus", "gladiator", "greetings"]
        }
    ]
    
    print("🧪 Testing Enhanced Chronoverse System")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}")
        print(f"   Query: '{test['data']['user_text']}'")
        
        start_time = time.time()
        
        try:
            response = requests.post(base_url, data=test['data'])
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                response_text = result['response_text']
                
                print(f"   ✅ Response ({response_time:.2f}s): '{response_text[:100]}...'")
                
                # Check for expected keywords
                found_keywords = [kw for kw in test['expected_keywords'] 
                                if kw.lower() in response_text.lower()]
                
                if found_keywords:
                    print(f"   🎯 Found keywords: {found_keywords}")
                else:
                    print(f"   ⚠️ Expected keywords not found: {test['expected_keywords']}")
                    
            else:
                print(f"   ❌ Failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"\n🎉 Enhanced System Testing Complete!")

if __name__ == "__main__":
    test_enhanced_chronoverse()
