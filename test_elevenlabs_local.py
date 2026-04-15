"""
Local ElevenLabs API Test Script
Run this script locally to verify ElevenLabs API connectivity
"""
import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables from .env.local
def load_env_local():
    env_path = Path(__file__).parent / '.env.local'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def test_elevenlabs():
    """Test ElevenLabs API connectivity"""
    print("=" * 60)
    print("ElevenLabs API Test - Local Environment")
    print("=" * 60)
    
    # Load environment variables
    load_env_local()
    
    api_key = os.environ.get('ELEVENLABS_API_KEY')
    voice_id = os.environ.get('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')
    
    # Test 1: Check if API key is configured
    print("\n[TEST 1] Checking API Key Configuration...")
    if not api_key:
        print("❌ FAILED: ELEVENLABS_API_KEY not found in environment")
        print("   Please set it in .env.local file")
        return False
    print(f"✓ API key is configured (length: {len(api_key)} chars)")
    
    # Test 2: Verify API key by fetching user info
    print("\n[TEST 2] Verifying API Key with ElevenLabs...")
    try:
        user_req = urllib.request.Request(
            'https://api.elevenlabs.io/v1/user',
            headers={'xi-api-key': api_key}
        )
        with urllib.request.urlopen(user_req, timeout=10) as response:
            user_data = json.loads(response.read().decode())
        
        print("✓ API key is valid!")
        subscription = user_data.get('subscription', {})
        print(f"  - Character count: {subscription.get('character_count', 0)}")
        print(f"  - Character limit: {subscription.get('character_limit', 0)}")
        
    except urllib.error.HTTPError as e:
        print(f"❌ FAILED: HTTP {e.code} - {e.reason}")
        print(f"   API key may be invalid or expired")
        return False
    except urllib.error.URLError as e:
        print(f"❌ FAILED: Network error - {e.reason}")
        print(f"   Cannot reach ElevenLabs servers")
        return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    
    # Test 3: Fetch available voices
    print("\n[TEST 3] Fetching Available Voices...")
    try:
        voices_req = urllib.request.Request(
            'https://api.elevenlabs.io/v1/voices',
            headers={'xi-api-key': api_key}
        )
        with urllib.request.urlopen(voices_req, timeout=10) as response:
            voices_data = json.loads(response.read().decode())
        
        voices = voices_data.get('voices', [])
        print(f"✓ Found {len(voices)} available voices")
        
        # Check if configured voice exists
        voice_exists = any(v['voice_id'] == voice_id for v in voices)
        if voice_exists:
            voice_name = next(v['name'] for v in voices if v['voice_id'] == voice_id)
            print(f"✓ Configured voice '{voice_name}' ({voice_id}) exists")
        else:
            print(f"⚠ WARNING: Configured voice ID {voice_id} not found")
            print(f"  Available voices:")
            for v in voices[:5]:  # Show first 5
                print(f"    - {v['name']} ({v['voice_id']})")
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    
    # Test 4: Test text-to-speech conversion
    print("\n[TEST 4] Testing Text-to-Speech Conversion...")
    try:
        test_text = "This is a test of the ElevenLabs text to speech system."
        tts_url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
        tts_data = json.dumps({
            'text': test_text,
            'model_id': 'eleven_monolingual_v1'
        }).encode('utf-8')
        
        tts_req = urllib.request.Request(
            tts_url,
            data=tts_data,
            headers={
                'xi-api-key': api_key,
                'Content-Type': 'application/json'
            }
        )
        
        with urllib.request.urlopen(tts_req, timeout=15) as response:
            audio_data = response.read()
        
        print(f"✓ Text-to-speech conversion successful!")
        print(f"  - Generated {len(audio_data)} bytes of audio data")
        print(f"  - Text: '{test_text}'")
        
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else 'No details'
        print(f"❌ FAILED: HTTP {e.code} - {e.reason}")
        print(f"   {error_body}")
        return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    
    # All tests passed
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("ElevenLabs API is properly configured and accessible")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_elevenlabs()
    exit(0 if success else 1)
