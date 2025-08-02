import requests
import time
import json

def test_tts_integration():
    base_url = "http://localhost:8000/api/v1/dialogue"
    
    print("🎤 Testing Chronoverse TTS Integration")
    print("=" * 60)
    
    # Test conversations designed to showcase character voices
    test_conversations = [
        {
            "name": "Marcus - Combat Authority",
            "character_id": "roman_gladiator",
            "user_text": "Tell me about your most dangerous gladiator battle"
        },
        {
            "name": "Ahmad - Architectural Wisdom", 
            "character_id": "mughal_architect",
            "user_text": "How did you design the beautiful dome of the Taj Mahal?"
        },
        {
            "name": "Khaemwaset - Scholarly Knowledge",
            "character_id": "egyptian_scribe", 
            "user_text": "Explain the sacred meaning of hieroglyphic writing"
        },
        {
            "name": "Marcus - Quick Greeting",
            "character_id": "roman_gladiator",
            "user_text": "Hello Marcus, nice to meet you"
        }
    ]
    
    for i, test in enumerate(test_conversations, 1):
        print(f"\n{i}. Testing: {test['name']}")
        print(f"   Character: {test['character_id']}")
        print(f"   Query: '{test['user_text']}'")
        
        start_time = time.time()
        
        try:
            response = requests.post(base_url, data={
                "character_id": test["character_id"],
                "user_text": test["user_text"]
            })
            
            total_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"   ✅ Status: Success")
                print(f"   📝 Response: '{result['response_text'][:80]}...'")
                print(f"   ⏱️ Processing Time: {result['processing_time_ms']}ms")
                print(f"   🌐 Total Request Time: {total_time:.2f}s")
                
                # Check TTS integration
                if result.get('audio_url'):
                    print(f"   🎵 Audio Generated: {result['audio_url']}")
                    print(f"   🔊 Voice File Ready: ✅")
                    
                    # Try to access audio file info
                    audio_check_url = f"http://localhost:8000{result['audio_url']}"
                    print(f"   🔗 Audio Access URL: {audio_check_url}")
                else:
                    print(f"   ❌ No audio generated")
                
                # Check session continuity
                if result.get('session_id'):
                    print(f"   🧠 Session ID: {result['session_id'][:8]}...")
                
            else:
                print(f"   ❌ Request Failed: {response.status_code}")
                print(f"   📄 Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        print(f"   " + "-" * 50)
        time.sleep(1)  # Brief pause between tests
    
    print(f"\n🎉 TTS Integration Testing Complete!")
    
    # Summary and next steps
    print(f"\n📋 TESTING SUMMARY:")
    print(f"   • Test character voices in order of speaking style")
    print(f"   • Check audio file generation and accessibility") 
    print(f"   • Verify TTS integration doesn't break dialogue flow")
    print(f"   • Confirm session memory works with TTS")
    
    print(f"\n🎧 TO HEAR THE VOICES:")
    print(f"   1. Look for audio URLs in the test output above")
    print(f"   2. Visit: http://localhost:8000/audio/[filename].wav")
    print(f"   3. Play the audio files to hear each character's voice")
    
    print(f"\n🚀 EXPECTED VOICE CHARACTERISTICS:")
    print(f"   • Marcus: Deep, commanding, authoritative tone")
    print(f"   • Ahmad: Wise, contemplative, measured speech")  
    print(f"   • Khaemwaset: Formal, scholarly, precise pronunciation")

if __name__ == "__main__":
    test_tts_integration()
