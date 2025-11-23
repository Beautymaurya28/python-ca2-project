"""
Pipoo Desktop Assistant - Configuration Manager
Handles all configuration settings, environment variables, and constants
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Central configuration class for Pipoo Assistant
    """
    
    # ==================== PROJECT PATHS ====================
    BASE_DIR = Path(__file__).parent.parent
    ASSETS_DIR = BASE_DIR / 'assets'
    ICONS_DIR = ASSETS_DIR / 'icons'
    SOUNDS_DIR = ASSETS_DIR / 'sounds'
    
    # ==================== API CONFIGURATION ====================
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent'

    
    # API request settings
    API_TIMEOUT = 30  # seconds
    MAX_RETRIES = 3
    
    # ==================== ASSISTANT SETTINGS ====================
    ASSISTANT_NAME = os.getenv('ASSISTANT_NAME', 'Pipoo')
    VERSION = '1.0.0'
    
    # Assistant personality
    SYSTEM_PROMPT = f"""You are {ASSISTANT_NAME}, a friendly and helpful AI assistant.
You are cute, cheerful, and always eager to help. Keep responses concise and friendly.
Use emojis occasionally to add personality. Be supportive and encouraging."""
    
    # ==================== VOICE SETTINGS ====================
    # Speech Recognition
    # More forgiving speech settings
    SPEECH_RECOGNITION_TIMEOUT = 15  # Longer timeout
    SPEECH_RECOGNITION_PHRASE_LIMIT = 20  # Longer phrases
    SPEECH_LANGUAGE = 'en-US'
    
    # Text-to-Speech
    TTS_RATE = int(os.getenv('SPEECH_RATE', 170))  # Words per minute
    TTS_VOLUME = 1.0  # 0.0 to 1.0
    TTS_VOICE_GENDER = os.getenv('VOICE_GENDER', 'female')
    
    # ==================== UI SETTINGS ====================
    # Window dimensions
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 700
    WINDOW_MIN_WIDTH = 700
    WINDOW_MIN_HEIGHT = 500
    
    # Colors (Cute Robot Theme)
    COLORS = {
        'primary': '#4A90E2',       # Soft Blue
        'secondary': '#7B68EE',     # Medium Slate Blue
        'accent': '#FF6B9D',        # Cute Pink
        'background': '#2C3E50',    # Dark Blue-Grey
        'surface': '#34495E',       # Lighter Grey
        'surface_light': '#445566', # Even Lighter
        'text': '#ECF0F1',          # Off-White
        'text_dim': '#BDC3C7',      # Dimmed text
        'success': '#2ECC71',       # Green
        'warning': '#F39C12',       # Orange
        'error': '#E74C3C',         # Red
        'listening': '#3498DB',     # Bright Blue
        'speaking': '#9B59B6',      # Purple
        'thinking': '#1ABC9C',      # Turquoise
    }
    
    # Font settings
    FONT_FAMILY = 'Segoe UI'
    FONT_SIZE_NORMAL = 11
    FONT_SIZE_LARGE = 14
    FONT_SIZE_TITLE = 18
    
    # Chat settings
    MAX_CHAT_HISTORY = 100  # Maximum messages to keep in UI
    CHAT_BUBBLE_PADDING = 15
    
    # ==================== ANIMATION SETTINGS ====================
    # Waveform animation
    WAVEFORM_BARS = 20
    WAVEFORM_UPDATE_MS = 50  # milliseconds
    WAVEFORM_HEIGHT = 60
    
    # Pulse animation (idle state)
    PULSE_SPEED_MS = 100  # milliseconds per frame
    PULSE_FRAMES = ['○', '◔', '◑', '◕', '●', '◕', '◑', '◔']
    
    # Typing animation
    TYPING_DOTS = ['   ', '.  ', '.. ', '...']
    TYPING_SPEED_MS = 400  # milliseconds per frame
    
    # ==================== LOGGING ====================
    LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
    ENABLE_CONSOLE_LOGS = True
    
    # ==================== FEATURES FLAGS ====================
    ENABLE_SOUND_EFFECTS = False  # Set to True if you add sound files
    ENABLE_WAKE_WORD = False      # Future feature
    SAVE_CHAT_HISTORY = True      # Save conversations to file
    
    # ==================== VALIDATION ====================
    @classmethod
    def validate(cls):
        """
        Validate configuration and check for required settings
        Returns: tuple (is_valid: bool, error_message: str)
        """
        errors = []
        
        # Check API key
        if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == 'your_api_key_here':
            errors.append("Gemini API key not configured. Please set GEMINI_API_KEY in .env file")
        
        # Check if .env exists
        env_path = cls.BASE_DIR / '.env'
        if not env_path.exists():
            errors.append(".env file not found. Copy .env.example to .env and configure it")
        
        # Create assets directories if they don't exist
        cls.ASSETS_DIR.mkdir(exist_ok=True)
        cls.ICONS_DIR.mkdir(exist_ok=True)
        cls.SOUNDS_DIR.mkdir(exist_ok=True)
        
        if errors:
            return False, "\n".join(errors)
        
        return True, "Configuration valid"
    
    @classmethod
    def get_info(cls):
        """
        Get configuration information for display
        """
        return {
            'Assistant Name': cls.ASSISTANT_NAME,
            'Version': cls.VERSION,
            'API Configured': 'Yes' if cls.GEMINI_API_KEY else 'No',
            'Speech Language': cls.SPEECH_LANGUAGE,
            'TTS Rate': f"{cls.TTS_RATE} WPM",
        }


class AppState:
    """
    Runtime state management for the application
    """
    
    def __init__(self):
        self.is_listening = False
        self.is_speaking = False
        self.is_thinking = False
        self.is_running = True
        self.current_animation = 'idle'
        self.last_user_input = ''
        self.last_assistant_response = ''
        self.conversation_history = []
        self.error_message = None
    
    def set_listening(self, value: bool):
        """Set listening state and update animation"""
        self.is_listening = value
        self.current_animation = 'listening' if value else 'idle'
    
    def set_speaking(self, value: bool):
        """Set speaking state and update animation"""
        self.is_speaking = value
        self.current_animation = 'speaking' if value else 'idle'
    
    def set_thinking(self, value: bool):
        """Set thinking state and update animation"""
        self.is_thinking = value
        self.current_animation = 'thinking' if value else 'idle'
    
    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': self._get_timestamp()
        })
        
        # Keep only last MAX_CHAT_HISTORY messages
        if len(self.conversation_history) > Config.MAX_CHAT_HISTORY:
            self.conversation_history = self.conversation_history[-Config.MAX_CHAT_HISTORY:]
    
    def get_conversation_for_api(self, limit: int = 10):
        """
        Get recent conversation history formatted for API
        """
        recent = self.conversation_history[-limit:]
        return [
            {'role': msg['role'], 'content': msg['content']}
            for msg in recent
        ]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    @staticmethod
    def _get_timestamp():
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime('%H:%M:%S')


# Global state instance
app_state = AppState()


# ==================== UTILITY FUNCTIONS ====================

def get_greeting():
    """Get time-appropriate greeting"""
    from datetime import datetime
    hour = datetime.now().hour
    
    if hour < 12:
        return f"Good morning! I'm {Config.ASSISTANT_NAME}, ready to help! 🌅"
    elif hour < 18:
        return f"Good afternoon! I'm {Config.ASSISTANT_NAME}, what can I do for you? ☀️"
    else:
        return f"Good evening! I'm {Config.ASSISTANT_NAME}, here to assist! 🌙"


def format_error_message(error: Exception) -> str:
    """Format error message for user display"""
    error_str = str(error)
    
    # Make error messages user-friendly
    if 'API_KEY' in error_str.upper():
        return "⚠️ API key issue. Please check your configuration."
    elif 'TIMEOUT' in error_str.upper():
        return "⏱️ Request timed out. Please try again."
    elif 'CONNECTION' in error_str.upper() or 'NETWORK' in error_str.upper():
        return "🌐 Network error. Please check your internet connection."
    elif 'MICROPHONE' in error_str.upper():
        return "🎤 Microphone error. Please check your microphone."
    else:
        return f"❌ Error: {error_str}"


if __name__ == '__main__':
    # Test configuration
    print("="*50)
    print("Pipoo Configuration Test")
    print("="*50)
    
    is_valid, message = Config.validate()
    print(f"\nValidation: {'✓ PASS' if is_valid else '✗ FAIL'}")
    print(f"Message: {message}\n")
    
    print("Configuration Info:")
    for key, value in Config.get_info().items():
        print(f"  {key}: {value}")
    
    print(f"\nGreeting: {get_greeting()}")
    print("\n" + "="*50)