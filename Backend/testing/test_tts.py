import requests
import time

def test_working_tts():
    """Test the working free TTS solution"""
    
    tests = [
        ("roman_gladiator", "Salve! I am Marcus Quintus, veteran of the arena!"),
        ("medieval_knight", "Hail and well met! I am Sir Gareth of Camelot."),
        ("mughal_architect", "Peace be upon you. I design with divine inspiration."),
        ("egyptian_scribe", "Greetings, seeker of wisdom and knowledge.")
    ]
    
    print("🎤 Testing Working Free TTS Solution")
    print("=" * 50)
    
    for character_id, text in tests:
        print(f"\n🎭 Testing {character_id}...")
        print(f"   Text: '{text}'")
        
        start = time.time()
        response = requests.post("http://localhost:8000/api/v1/dialogue", data={
            "character_id": character_id,
            "user_text": text
        })
        duration = time.time() - start
        
        if response.status_code == 200:
            result = response.json()
            if result.get('audio_url'):
                print(f"   ✅ Success in {duration:.1f}s")
                print(f"   🎵 Audio: {result['audio_url']}")
                print(f"   📝 Response: {result['response_text'][:60]}...")
            else:
                print(f"   ❌ No audio generated")
                print(f"   📝 Response: {result['response_text'][:60]}...")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    
    print(f"\n🎉 Free TTS testing complete!")
    print(f"🎧 Check generated_audio/ folder for voice files!")

if __name__ == "__main__":
    test_working_tts()
