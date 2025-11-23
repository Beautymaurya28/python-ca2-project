"""
Pipoo Desktop Assistant - Voice Handler (COMPLETE FIXED VERSION)
Manages speech recognition (input) and text-to-speech (output)
"""

import speech_recognition as sr
import pyttsx3
import threading
from typing import Optional, Callable
from config import Config, format_error_message


class VoiceHandler:
    """
    Handles all voice-related operations:
    - Speech recognition (microphone input)
    - Text-to-speech output
    - Audio device management
    """
    
    def __init__(self):
        """Initialize voice handler with recognizer and TTS engine"""
        # Speech Recognition
        self.recognizer = sr.Recognizer()
        self.microphone = None
        
        # Text-to-Speech
        self.tts_engine = None
        self.is_speaking = False
        self.is_listening = False
        
        # Callbacks
        self.on_listen_start: Optional[Callable] = None
        self.on_listen_end: Optional[Callable] = None
        self.on_speak_start: Optional[Callable] = None
        self.on_speak_end: Optional[Callable] = None
        
        # Initialize TTS
        self._init_tts()
        
        # Initialize microphone
        self._init_microphone()
    
    def _init_tts(self):
        """Initialize text-to-speech engine"""
        try:
            self.tts_engine = pyttsx3.init()
            
            # Set voice properties
            self.tts_engine.setProperty('rate', Config.TTS_RATE)
            self.tts_engine.setProperty('volume', Config.TTS_VOLUME)
            
            # Try to set voice gender (optional, may not work on all systems)
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find female voice if requested
                if Config.TTS_VOICE_GENDER.lower() == 'female':
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                else:
                    # Use first available voice
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            print("✓ Text-to-Speech initialized")
            
        except Exception as e:
            print(f"✗ TTS initialization error: {e}")
            self.tts_engine = None
    
    def _init_microphone(self):
        """Initialize microphone with improved settings"""
        try:
            # Initialize microphone (use default device)
            self.microphone = sr.Microphone()
            
            # Calibrate for ambient noise with better settings
            with self.microphone as source:
                print("🎤 Calibrating microphone (please be quiet for 2 seconds)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                
                # Set more sensitive recognition settings
                self.recognizer.energy_threshold = 300  # Lower = more sensitive (default ~4000)
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.dynamic_energy_adjustment_damping = 0.15
                self.recognizer.dynamic_energy_ratio = 1.5
                self.recognizer.pause_threshold = 0.8  # Seconds of silence to consider phrase complete
                
                print(f"   ✓ Energy threshold set to: {self.recognizer.energy_threshold}")
                print(f"   ✓ Pause threshold: {self.recognizer.pause_threshold}s")
            
            print("✓ Microphone initialized and calibrated")
            
        except Exception as e:
            print(f"✗ Microphone initialization error: {e}")
            print("   Please check:")
            print("   - Microphone is connected")
            print("   - Microphone permissions are enabled")
            print("   - No other app is using the microphone")
            self.microphone = None
    
    def listen(self, timeout: int = None) -> Optional[str]:
        """
        Listen for speech input from microphone
        
        Args:
            timeout: Maximum seconds to wait for speech (None = use config default)
            
        Returns:
            Recognized text or None if failed
        """
        if not self.microphone:
            print("❌ No microphone available")
            return None
        
        self.is_listening = True
        if self.on_listen_start:
            self.on_listen_start()
        
        try:
            with self.microphone as source:
                print("🎤 Listening... (speak now!)")
                
                # Brief ambient noise adjustment
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                
                # Set timeout
                listen_timeout = timeout or Config.SPEECH_RECOGNITION_TIMEOUT
                
                print(f"⏳ Waiting up to {listen_timeout} seconds for speech...")
                
                # Listen for audio with increased sensitivity
                audio = self.recognizer.listen(
                    source,
                    timeout=listen_timeout,
                    phrase_time_limit=Config.SPEECH_RECOGNITION_PHRASE_LIMIT
                )
                
                print("🔄 Processing speech... (connecting to Google)")
                
                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(
                    audio,
                    language=Config.SPEECH_LANGUAGE,
                    show_all=False
                )
                
                print(f"✓ Recognized: {text}")
                return text
                
        except sr.WaitTimeoutError:
            print("⏱️ Listening timeout - no speech detected")
            print("💡 TIP: Speak louder and closer to the microphone!")
            return None
            
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            print("💡 TIP: Speak more clearly and reduce background noise!")
            return None
            
        except sr.RequestError as e:
            print(f"❌ Speech recognition service error: {e}")
            print("💡 TIP: Check your internet connection!")
            return None
            
        except Exception as e:
            print(f"❌ Listening error: {e}")
            return None
            
        finally:
            self.is_listening = False
            if self.on_listen_end:
                self.on_listen_end()
    
    def listen_continuous(self, duration: int = 10) -> Optional[str]:
        """
        Listen continuously for a longer duration (good for longer sentences)
        
        Args:
            duration: How long to listen in seconds
            
        Returns:
            Recognized text or None
        """
        if not self.microphone:
            return None
        
        self.is_listening = True
        if self.on_listen_start:
            self.on_listen_start()
        
        try:
            with self.microphone as source:
                print(f"🎤 Listening continuously for {duration} seconds...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Record for specified duration
                audio = self.recognizer.record(source, duration=duration)
                
                print("🔄 Processing recorded audio...")
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio, language=Config.SPEECH_LANGUAGE)
                
                print(f"✓ Recognized: {text}")
                return text
                
        except Exception as e:
            print(f"❌ Error in continuous listening: {e}")
            return None
            
        finally:
            self.is_listening = False
            if self.on_listen_end:
                self.on_listen_end()
    
    def speak(self, text: str, blocking: bool = False):
        """
        Speak text using TTS
        
        Args:
            text: Text to speak
            blocking: If True, wait for speech to complete
        """
        if not self.tts_engine or not text:
            print("⚠️ TTS not available or no text to speak")
            return
        
        def _speak():
            self.is_speaking = True
            if self.on_speak_start:
                self.on_speak_start()
            
            try:
                print(f"🔊 Speaking: {text}")
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                
            except Exception as e:
                print(f"❌ TTS error: {e}")
                
            finally:
                self.is_speaking = False
                if self.on_speak_end:
                    self.on_speak_end()
        
        if blocking:
            _speak()
        else:
            # Speak in separate thread to avoid blocking UI
            speak_thread = threading.Thread(target=_speak, daemon=True)
            speak_thread.start()
    
    def stop_speaking(self):
        """Stop current speech"""
        if self.tts_engine and self.is_speaking:
            try:
                self.tts_engine.stop()
                self.is_speaking = False
                print("⏹️ Speech stopped")
            except Exception as e:
                print(f"❌ Error stopping speech: {e}")
    
    def test_microphone(self) -> bool:
        """
        Test if microphone is working
        
        Returns:
            True if microphone is accessible
        """
        try:
            if not self.microphone:
                return False
            
            with self.microphone as source:
                # Try to access microphone briefly
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            
            print("✓ Microphone test passed")
            return True
            
        except Exception as e:
            print(f"✗ Microphone test failed: {e}")
            return False
    
    def test_tts(self) -> bool:
        """
        Test if TTS is working
        
        Returns:
            True if TTS is accessible
        """
        try:
            if not self.tts_engine:
                return False
            
            # Try to initialize TTS
            voices = self.tts_engine.getProperty('voices')
            result = len(voices) > 0
            
            if result:
                print("✓ TTS test passed")
            else:
                print("✗ TTS test failed: No voices available")
            
            return result
            
        except Exception as e:
            print(f"✗ TTS test failed: {e}")
            return False
    
    def list_microphones(self):
        """List all available microphones"""
        try:
            print("\n📋 Available Microphones:")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"   {index}: {name}")
            print()
        except Exception as e:
            print(f"❌ Error listing microphones: {e}")
    
    def set_microphone(self, device_index: int):
        """
        Set specific microphone by index
        
        Args:
            device_index: Index of the microphone to use
        """
        try:
            self.microphone = sr.Microphone(device_index=device_index)
            
            # Re-calibrate
            with self.microphone as source:
                print(f"🎤 Using microphone index {device_index}")
                print("   Calibrating...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
            
            print(f"✓ Microphone {device_index} set and calibrated")
            
        except Exception as e:
            print(f"❌ Error setting microphone: {e}")
    
    def adjust_sensitivity(self, sensitivity: str = 'medium'):
        """
        Adjust microphone sensitivity
        
        Args:
            sensitivity: 'low', 'medium', 'high', or 'very_high'
        """
        sensitivity_map = {
            'low': 4000,
            'medium': 2000,
            'high': 1000,
            'very_high': 300
        }
        
        threshold = sensitivity_map.get(sensitivity, 2000)
        self.recognizer.energy_threshold = threshold
        
        print(f"🔊 Sensitivity set to: {sensitivity} (threshold: {threshold})")
    
    def get_status(self) -> dict:
        """
        Get current voice handler status
        
        Returns:
            Dictionary with status information
        """
        return {
            'microphone_available': self.microphone is not None,
            'tts_available': self.tts_engine is not None,
            'is_listening': self.is_listening,
            'is_speaking': self.is_speaking,
            'microphone_test': self.test_microphone(),
            'tts_test': self.test_tts(),
            'energy_threshold': self.recognizer.energy_threshold,
            'pause_threshold': self.recognizer.pause_threshold
        }
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.tts_engine:
                self.tts_engine.stop()
            print("✓ Voice handler cleaned up")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")


# ==================== TESTING ====================

if __name__ == '__main__':
    """Test voice handler functionality"""
    
    print("="*60)
    print("Pipoo Voice Handler Test")
    print("="*60)
    
    # Initialize
    voice = VoiceHandler()
    
    # List available microphones
    voice.list_microphones()
    
    # Get status
    print("\n📊 Voice Handler Status:")
    status = voice.get_status()
    for key, value in status.items():
        symbol = "✓" if value else "✗"
        print(f"  {symbol} {key}: {value}")
    
    # Test TTS
    print("\n" + "="*60)
    print("Testing Text-to-Speech...")
    print("="*60)
    voice.speak("Hello! I am Pipoo, your friendly AI assistant!", blocking=True)
    
    # Test microphone
    print("\n" + "="*60)
    print("Testing Microphone - SAY SOMETHING NOW!")
    print("(You have 10 seconds)")
    print("="*60)
    
    try:
        result = voice.listen(timeout=10)
        if result:
            print(f"\n✓ SUCCESS! You said: '{result}'")
            voice.speak(f"I heard you say: {result}", blocking=True)
        else:
            print("\n✗ No speech detected or error occurred")
            print("\nTroubleshooting tips:")
            print("  1. Check if microphone is connected")
            print("  2. Check Windows microphone permissions")
            print("  3. Speak louder and closer to microphone")
            print("  4. Reduce background noise")
            print("  5. Try running: python -m speech_recognition")
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    
    # Show final status
    print("\n" + "="*60)
    print("Final Status:")
    status = voice.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Cleanup
    voice.cleanup()
    
    print("\n" + "="*60)
    print("Test complete!")
    print("="*60)