"""
Pipoo Desktop Assistant - Gemini API Handler (FIXED)
Manages communication with Google's Gemini AI API
"""

import requests
import json
from typing import Optional, List, Dict
from config import Config, format_error_message
import time


class GeminiAPI:
    """
    Handles all interactions with Google Gemini API
    - Send queries and get responses
    - Manage conversation context
    - Handle errors and retries
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Gemini API handler
        
        Args:
            api_key: Google Gemini API key (uses Config if not provided)
        """
        self.api_key = api_key or Config.GEMINI_API_KEY
        self.conversation_history = []
        self.request_count = 0
        
        # Validate API key
        if not self.api_key or self.api_key == 'your_api_key_here':
            raise ValueError("Invalid Gemini API key. Please configure in .env file")
        
        print("✓ Gemini API initialized")
    
    def _build_request_body(self, prompt: str, use_history: bool = True) -> dict:
        """
        Build request body for Gemini API
        
        Args:
            prompt: User's input text
            use_history: Include conversation history
            
        Returns:
            Request body dictionary
        """
        # Build the full prompt with context
        full_prompt = Config.SYSTEM_PROMPT + "\n\n"
        
        # Add conversation history if enabled
        if use_history and self.conversation_history:
            for msg in self.conversation_history[-10:]:  # Last 10 messages
                full_prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
        
        # Add current prompt
        full_prompt += f"User: {prompt}\nAssistant:"
        
        # Build request body
        request_body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": full_prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.9,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        return request_body
    
    def query(self, prompt: str, use_history: bool = True, retry_count: int = 0) -> Optional[str]:
        """
        Send query to Gemini API and get response
        
        Args:
            prompt: User's question/input
            use_history: Include conversation context
            retry_count: Current retry attempt (internal use)
            
        Returns:
            AI response text or None if failed
        """
        try:
            # Build API URL with key
            url = f"{Config.GEMINI_API_URL}?key={self.api_key}"
            
            # Build request body
            request_body = self._build_request_body(prompt, use_history)
            
            # Make API request
            print(f"🌐 Sending request to Gemini API... (attempt {retry_count + 1})")
            
            response = requests.post(
                url,
                headers={'Content-Type': 'application/json'},
                json=request_body,
                timeout=Config.API_TIMEOUT
            )
            
            # Debug: Print response for troubleshooting
            print(f"📡 Response Status: {response.status_code}")
            
            # Check response status
            if response.status_code == 200:
                # Parse response
                data = response.json()
                
                # Extract text from response
                if 'candidates' in data and len(data['candidates']) > 0:
                    candidate = data['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        parts = candidate['content']['parts']
                        if len(parts) > 0 and 'text' in parts[0]:
                            text = parts[0]['text'].strip()
                            
                            # Update conversation history
                            self.add_to_history('user', prompt)
                            self.add_to_history('assistant', text)
                            
                            self.request_count += 1
                            print(f"✓ Received response ({len(text)} chars)")
                            
                            return text
                
                # No valid response found
                print(f"⚠️ Unexpected response structure: {data}")
                return "I'm sorry, I couldn't generate a response. Please try again."
            
            elif response.status_code == 429:
                # Rate limit exceeded
                if retry_count < Config.MAX_RETRIES:
                    wait_time = 2 ** retry_count  # Exponential backoff
                    print(f"⏱️ Rate limit hit, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                    return self.query(prompt, use_history, retry_count + 1)
                else:
                    return "⚠️ API rate limit exceeded. Please wait a moment and try again."
            
            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Bad request')
                    print(f"❌ API Error (400): {error_msg}")
                    return f"⚠️ Request error: {error_msg}"
                except:
                    print(f"❌ API Error (400): Bad request")
                    return "⚠️ Bad request. Please try again."
            
            elif response.status_code == 403:
                return "⚠️ API key error. Please check your Gemini API key configuration."
            
            elif response.status_code == 404:
                print(f"❌ API Error (404): Endpoint not found")
                print(f"🔍 Current URL: {url}")
                return "⚠️ API endpoint error. Please check the API URL configuration."
            
            else:
                print(f"❌ API Error: Status {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"📄 Error details: {error_detail}")
                except:
                    pass
                return f"⚠️ API error (code {response.status_code}). Please try again."
        
        except requests.exceptions.Timeout:
            print("⏱️ Request timeout")
            if retry_count < Config.MAX_RETRIES:
                return self.query(prompt, use_history, retry_count + 1)
            return "⏱️ Request timed out. Please check your internet connection."
        
        except requests.exceptions.ConnectionError:
            print("🌐 Connection error")
            return "🌐 Cannot connect to Gemini API. Please check your internet connection."
        
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return format_error_message(e)
    
    def add_to_history(self, role: str, content: str):
        """
        Add message to conversation history
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        self.conversation_history.append({
            'role': role,
            'content': content
        })
        
        # Keep only last 50 messages to manage memory
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("🗑️ Conversation history cleared")
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get conversation history
        
        Returns:
            List of message dictionaries
        """
        return self.conversation_history
    
    def get_stats(self) -> dict:
        """
        Get API usage statistics
        
        Returns:
            Dictionary with statistics
        """
        return {
            'total_requests': self.request_count,
            'history_length': len(self.conversation_history),
            'api_configured': bool(self.api_key and self.api_key != 'your_api_key_here')
        }
    
    def test_connection(self) -> bool:
        """
        Test API connection with simple query
        
        Returns:
            True if connection successful
        """
        try:
            print("🧪 Testing Gemini API connection...")
            response = self.query("Say 'Hello' in one word.", use_history=False)
            
            if response and not response.startswith('⚠️') and not response.startswith('❌'):
                print("✓ API connection test passed")
                print(f"✓ Response: {response}")
                return True
            else:
                print("⚠️ API test failed or returned error")
                return False
                
        except Exception as e:
            print(f"✗ API connection test failed: {e}")
            return False


# ==================== TESTING ====================

if __name__ == '__main__':
    """Test Gemini API functionality"""
    
    print("="*60)
    print("Pipoo Gemini API Test")
    print("="*60)
    
    try:
        # Initialize API
        gemini = GeminiAPI()
        
        # Get stats
        print("\nAPI Statistics:")
        stats = gemini.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Test connection
        print("\n" + "="*60)
        print("Testing API Connection...")
        print("="*60)
        
        if gemini.test_connection():
            print("\n✓ Connection test passed!")
            
            # Test actual query
            print("\n" + "="*60)
            print("Testing Full Query...")
            print("="*60)
            
            test_query = "Tell me a very short joke about robots."
            print(f"\nQuery: {test_query}")
            
            response = gemini.query(test_query)
            print(f"\nResponse: {response}")
            
            # Show updated stats
            print("\n" + "="*60)
            print("Updated Statistics:")
            stats = gemini.get_stats()
            for key, value in stats.items():
                print(f"  {key}: {value}")
        else:
            print("\n✗ Connection test failed.")
            print("\nTroubleshooting steps:")
            print("1. Check your API key in .env file")
            print("2. Verify internet connection")
            print("3. Visit: https://aistudio.google.com/app/apikey")
            print("4. Make sure API key has no extra spaces")
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure:")
        print("  1. .env file exists")
        print("  2. GEMINI_API_KEY is set in .env")
        print("  3. API key is valid")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("Test complete!")
    print("="*60)