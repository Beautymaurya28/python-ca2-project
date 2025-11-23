"""
Pipoo Desktop Assistant - Main Application
Brings together all components and handles application logic
"""

import tkinter as tk
import sys
import threading
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import Pipoo components
from config import Config, AppState, get_greeting, format_error_message
from voice_handler import VoiceHandler
from gemini_api import GeminiAPI
from ui_manager import UIManager
from automation_handler import AutomationHandler

# Banner
def print_banner():
    """Print Pipoo banner to console"""
    banner = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║   ██████╗ ██╗██████╗  ██████╗  ██████╗                   ║
║   ██╔══██╗██║██╔══██╗██╔═══██╗██╔═══██╗                  ║
║   ██████╔╝██║██████╔╝██║   ██║██║   ██║                  ║
║   ██╔═══╝ ██║██╔═══╝ ██║   ██║██║   ██║                  ║
║   ██║     ██║██║     ╚██████╔╝╚██████╔╝                  ║
║   ╚═╝     ╚═╝╚═╝      ╚═════╝  ╚═════╝                   ║
║                                                            ║
║            Your AI Robot Assistant                  ║
║                    Version 1.0.0                           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print()


class PipooAssistant:
    """
    Main controller for Pipoo Desktop Assistant
    Coordinates all components and manages application flow
    """
    
    def __init__(self):
        """Initialize Pipoo Assistant"""
        print_banner()
        print("Initializing Pipoo Assistant...")
        print("="*60)
        
        # Validate configuration
        is_valid, message = Config.validate()
        if not is_valid:
            print(f"\n❌ Configuration Error:")
            print(message)
            print("\nPlease fix the configuration and try again.")
            input("\nPress Enter to exit...")
            sys.exit(1)
        
        print(f"✓ Configuration valid")
        
        # Initialize components
        self.root = None
        self.ui = None
        self.voice = None
        self.gemini = None
        self.automation = None
        self.state = AppState()
        
        # Thread management
        self.processing_thread = None
        
        # Initialize UI
        self._init_ui()
        
        # Initialize voice handler
        self._init_voice()
        
        # Initialize Gemini API
        self._init_gemini()
        
        # Initialize automation handler
        self._init_automation()
        
        # Setup UI callbacks
        self._setup_callbacks()
        
        # Welcome message
        self._show_welcome()
        
        print("\n" + "="*60)
        print("✓ Pipoo is ready!")
        print("="*60 + "\n")
    
    def _init_ui(self):
        """Initialize user interface"""
        print("\nInitializing UI...")
        self.root = tk.Tk()
        self.ui = UIManager(self.root)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _init_voice(self):
        """Initialize voice handler"""
        print("Initializing voice systems...")
        try:
            self.voice = VoiceHandler()
            
            # Set callbacks for voice events
            self.voice.on_listen_start = self._on_listen_start
            self.voice.on_listen_end = self._on_listen_end
            self.voice.on_speak_start = self._on_speak_start
            self.voice.on_speak_end = self._on_speak_end
            
            # Check voice status
            status = self.voice.get_status()
            if not status['microphone_available']:
                self.ui.add_message('error', '⚠️ Microphone not available. Voice input disabled.')
            if not status['tts_available']:
                self.ui.add_message('error', '⚠️ Text-to-speech not available. Voice output disabled.')
                
        except Exception as e:
            print(f"❌ Voice initialization error: {e}")
            self.ui.add_message('error', f'Voice system error: {e}')
            self.voice = None
    
    def _init_gemini(self):
        """Initialize Gemini API"""
        print("Connecting to Gemini AI...")
        try:
            self.gemini = GeminiAPI()
            
            # Test connection
            if not self.gemini.test_connection():
                self.ui.add_message('error', '⚠️ Could not connect to Gemini API. Check your API key.')
                
        except ValueError as e:
            print(f"❌ Gemini API error: {e}")
            self.ui.add_message('error', str(e))
            self.gemini = None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            self.ui.add_message('error', format_error_message(e))
            self.gemini = None
    
    def _init_automation(self):
        """Initialize automation handler"""
        print("Initializing automation features...")
        try:
            self.automation = AutomationHandler()
            
            # Set callback for reminder notifications (if reminder system available)
            if hasattr(self, '_handle_reminder_notification'):
                self.automation.on_reminder_callback = self._handle_reminder_notification
            
        except Exception as e:
            print(f"❌ Automation error: {e}")
            self.ui.add_message('error', f'Automation system error: {e}')
            self.automation = None
    
    def _setup_callbacks(self):
        """Setup UI callbacks"""
        self.ui.on_speak_button = self.handle_speak_button
        self.ui.on_stop_button = self.handle_stop_button
        self.ui.on_clear_button = self.handle_clear_button
    
    def _show_welcome(self):
        """Show welcome message"""
        self.ui.show_greeting()
        self.ui.add_message('system', 'Click "🎤 Speak" to start talking!')
        self.ui.add_message('system', '✨ I can open apps, search the web, create notes, and chat with you!')
        self.ui.add_message('system', 'Try: "Open YouTube", "Search for cute cats", "Create a note"')
        self.ui.add_message('system', f'Powered by Google Gemini AI ✨')
    
    # ==================== VOICE EVENT HANDLERS ====================
    
    def _on_listen_start(self):
        """Called when listening starts"""
        self.root.after(0, lambda: self.ui.start_animation('listening'))
        self.root.after(0, lambda: self.ui.set_status("🎤 Listening...", Config.COLORS['listening']))
    
    def _on_listen_end(self):
        """Called when listening ends"""
        pass  # Will be handled by processing
    
    def _on_speak_start(self):
        """Called when speaking starts"""
        self.root.after(0, lambda: self.ui.start_animation('speaking'))
        self.root.after(0, lambda: self.ui.set_status("💬 Speaking...", Config.COLORS['speaking']))
    
    def _on_speak_end(self):
        """Called when speaking ends"""
        self.root.after(0, lambda: self.ui.start_animation('idle'))
        self.root.after(0, lambda: self.ui.set_status("🟢 Ready", Config.COLORS['success']))
        self.root.after(0, lambda: self.ui.set_buttons_enabled(True, False))
    
    # ==================== BUTTON HANDLERS ====================
    
    def handle_speak_button(self):
        """Handle speak button click"""
        if not self.voice:
            self.ui.add_message('error', '❌ Voice handler not available')
            return
        
        if not self.gemini:
            self.ui.add_message('error', '❌ Gemini API not available')
            return
        
        # Update UI
        self.ui.set_buttons_enabled(False, True)
        self.ui.set_status("🎤 Listening...", Config.COLORS['listening'])
        
        # Start processing in separate thread
        self.processing_thread = threading.Thread(target=self._process_voice_input, daemon=True)
        self.processing_thread.start()
    
    def handle_stop_button(self):
        """Handle stop button click"""
        # Stop speaking
        if self.voice and self.voice.is_speaking:
            self.voice.stop_speaking()
        
        # Reset UI
        self.ui.start_animation('idle')
        self.ui.set_status("⏹️ Stopped", Config.COLORS['warning'])
        self.ui.set_buttons_enabled(True, False)
        self.ui.add_message('system', 'Stopped')
    
    def handle_clear_button(self):
        """Handle clear button click"""
        # Clear chat UI
        self.ui.clear_chat()
        
        # Clear conversation history
        if self.gemini:
            self.gemini.clear_history()
        
        self.state.clear_history()
        
        # Show new greeting
        self._show_welcome()
    
    # ==================== VOICE PROCESSING ====================
    
    def _handle_reminder_notification(self, content: str, when: str, message: str):
        """Handle reminder notification when it triggers"""
        # Update UI
        self.root.after(0, lambda: self.ui.add_message('system', message))
        
        # Speak the reminder
        if self.voice:
            reminder_speech = f"Reminder! {content}"
            self.voice.speak(reminder_speech, blocking=False)
        
        # Show notification animation
        self.root.after(0, lambda: self.ui.start_animation('speaking'))
        self.root.after(0, lambda: self.ui.set_status("🔔 Reminder Alert!", Config.COLORS['warning']))
        
        # Return to idle after 3 seconds
        def back_to_idle():
            self.ui.start_animation('idle')
            self.ui.set_status("🟢 Ready", Config.COLORS['success'])
        
        self.root.after(3000, back_to_idle)
    
    def _process_voice_input(self):
        """Process voice input (runs in separate thread)"""
        try:
            # Listen for speech
            user_input = self.voice.listen(timeout=8)
            
            if not user_input:
                # No speech detected
                self.root.after(0, lambda: self.ui.add_message('system', '❓ No speech detected. Please try again.'))
                self.root.after(0, lambda: self.ui.set_buttons_enabled(True, False))
                self.root.after(0, lambda: self.ui.start_animation('idle'))
                self.root.after(0, lambda: self.ui.set_status("🟢 Ready", Config.COLORS['success']))
                return
            
            # Display user input
            self.root.after(0, lambda: self.ui.add_message('user', user_input))
            
            # Check if it's an automation command first
            if self.automation:
                is_command, command_response = self.automation.detect_and_execute(user_input)
                
                if is_command:
                    # It was a command, display response and speak it
                    self.root.after(0, lambda: self.ui.add_message('assistant', command_response))
                    self.state.add_message('user', user_input)
                    self.state.add_message('assistant', command_response)
                    
                    # Speak the response
                    self.voice.speak(command_response, blocking=False)
                    return
            
            # Not a command, ask Gemini AI
            self.root.after(0, lambda: self.ui.set_status("🤖 Thinking...", Config.COLORS['thinking']))
            self.root.after(0, lambda: self.ui.start_animation('thinking'))
            
            # Get AI response
            response = self.gemini.query(user_input)
            
            if response:
                # Display response
                self.root.after(0, lambda: self.ui.add_message('assistant', response))
                
                # Speak response
                self.voice.speak(response, blocking=False)
                
                # Add to state
                self.state.add_message('user', user_input)
                self.state.add_message('assistant', response)
            else:
                # Error getting response
                error_msg = "I'm sorry, I couldn't process that. Please try again."
                self.root.after(0, lambda: self.ui.add_message('error', error_msg))
                self.root.after(0, lambda: self.ui.set_buttons_enabled(True, False))
                self.root.after(0, lambda: self.ui.start_animation('idle'))
                self.root.after(0, lambda: self.ui.set_status("🟢 Ready", Config.COLORS['success']))
                
        except Exception as e:
            error_msg = format_error_message(e)
            self.root.after(0, lambda: self.ui.add_message('error', error_msg))
            self.root.after(0, lambda: self.ui.set_buttons_enabled(True, False))
            self.root.after(0, lambda: self.ui.start_animation('idle'))
            self.root.after(0, lambda: self.ui.set_status("❌ Error", Config.COLORS['error']))
    
    # ==================== APPLICATION CONTROL ====================
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n\nShutting down...")
            self.cleanup()
    
    def on_closing(self):
        """Handle window closing"""
        print("\nShutting down Pipoo...")
        self.cleanup()
        self.root.destroy()
    
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.voice:
                self.voice.cleanup()
            if self.ui:
                self.ui.cleanup()
            print("✓ Cleanup complete")
        except Exception as e:
            print(f"Cleanup warning: {e}")


# ==================== ENTRY POINT ====================

def main():
    """Main entry point"""
    try:
        # Create and run assistant
        assistant = PipooAssistant()
        assistant.run()
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        print("\nPlease check:")
        print("  1. All dependencies are installed (pip install -r requirements.txt)")
        print("  2. .env file exists with valid GEMINI_API_KEY")
        print("  3. Microphone is connected and working")
        print("  4. Internet connection is active")
        input("\nPress Enter to exit...")
        sys.exit(1)


if __name__ == '__main__':
    main()