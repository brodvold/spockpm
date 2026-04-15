"""
ElevenLabs API Test Endpoint
This endpoint tests connectivity to the ElevenLabs API to verify:
1. API key is properly configured
2. We can reach ElevenLabs servers
3. Voice ID is valid
"""
from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Test endpoint to verify ElevenLabs API connectivity.
        Returns status information about the API connection.
        """
        # Get API key from environment variables
        api_key = os.environ.get('ELEVENLABS_API_KEY')
        voice_id = os.environ.get('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM')  # Default voice
        
        # Check if API key is configured
        if not api_key:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                'success': False,
                'error': 'ELEVENLABS_API_KEY not configured',
                'message': 'Environment variable ELEVENLABS_API_KEY is missing'
            }
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Test 1: Verify API key by fetching user info
        try:
            user_req = urllib.request.Request(
                'https://api.elevenlabs.io/v1/user',
                headers={'xi-api-key': api_key}
            )
            with urllib.request.urlopen(user_req, timeout=10) as response:
                user_data = json.loads(response.read().decode())
            
            # Test 2: Verify voice exists by fetching voices
            voices_req = urllib.request.Request(
                'https://api.elevenlabs.io/v1/voices',
                headers={'xi-api-key': api_key}
            )
            with urllib.request.urlopen(voices_req, timeout=10) as response:
                voices_data = json.loads(response.read().decode())
            
            # Check if the configured voice_id exists
            voice_exists = any(v['voice_id'] == voice_id for v in voices_data.get('voices', []))
            
            # Test 3: Try a small text-to-speech conversion (test the actual TTS endpoint)
            test_text = "Test"
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
            
            tts_success = False
            tts_error = None
            try:
                with urllib.request.urlopen(tts_req, timeout=10) as response:
                    # We got audio data back, TTS works!
                    tts_success = True
            except urllib.error.HTTPError as e:
                tts_error = f"TTS test failed: {e.code} - {e.reason}"
            
            # Build successful response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            result = {
                'success': True,
                'message': 'ElevenLabs API is accessible',
                'details': {
                    'api_key_configured': True,
                    'api_key_valid': True,
                    'character_count': user_data.get('subscription', {}).get('character_count', 0),
                    'character_limit': user_data.get('subscription', {}).get('character_limit', 0),
                    'voice_id': voice_id,
                    'voice_exists': voice_exists,
                    'available_voices_count': len(voices_data.get('voices', [])),
                    'tts_test': 'success' if tts_success else 'failed',
                    'tts_error': tts_error
                },
                'environment': os.environ.get('VERCEL_ENV', 'local')
            }
            
            self.wfile.write(json.dumps(result, indent=2).encode())
            
        except urllib.error.HTTPError as e:
            # HTTP error from ElevenLabs API
            error_body = e.read().decode() if e.fp else 'No error details'
            self.send_response(502)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': False,
                'error': f'ElevenLabs API error: {e.code} - {e.reason}',
                'details': error_body,
                'message': 'Failed to communicate with ElevenLabs API - check API key validity'
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except urllib.error.URLError as e:
            # Network/connectivity error
            self.send_response(502)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': False,
                'error': f'Network error: {str(e.reason)}',
                'message': 'Could not reach ElevenLabs API - check internet connectivity'
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            # Unexpected error
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'message': 'An unexpected error occurred during testing'
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
