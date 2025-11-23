"""
Pipoo Desktop Assistant - UI Manager (FIXED)
Creates and manages the main graphical user interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, Canvas
from typing import Optional, Callable
from config import Config
from animations import AnimationManager
import threading


class UIManager:
    """
    Manages the main GUI for Pipoo Assistant:
    - Window creation and layout
    - Chat display
    - Control buttons
    - Status indicators
    - Animations integration
    """
    
    def __init__(self, root: tk.Tk):
        """
        Initialize UI Manager
        
        Args:
            root: Main Tkinter window
        """
        self.root = root
        self.animation_manager: Optional[AnimationManager] = None
        
        # Callbacks (to be set by main controller)
        self.on_speak_button: Optional[Callable] = None
        self.on_stop_button: Optional[Callable] = None
        self.on_clear_button: Optional[Callable] = None
        
        # UI elements
        self.chat_display = None
        self.status_label = None
        self.speak_button = None
        self.stop_button = None
        
        # Setup UI
        self._setup_window()
        self._create_widgets()
        
        print("✓ UI Manager initialized")
    
    def _setup_window(self):
        """Configure main window"""
        self.root.title(f"🤖 {Config.ASSISTANT_NAME} - Your Cute AI Assistant")
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.minsize(Config.WINDOW_MIN_WIDTH, Config.WINDOW_MIN_HEIGHT)
        
        # Set window icon (using emoji as fallback)
        try:
            self.root.iconbitmap(default='')  # Use default if no icon file
        except:
            pass
        
        # Configure colors
        self.root.configure(bg=Config.COLORS['background'])
        
        # Center window on screen
        self._center_window()
    
    def _center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = tk.Frame(self.root, bg=Config.COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # === TOP SECTION: Header ===
        self._create_header(main_frame)
        
        # === MIDDLE SECTION: Animation Canvas ===
        self._create_animation_area(main_frame)
        
        # === CHAT SECTION: Message Display ===
        self._create_chat_area(main_frame)
        
        # === BOTTOM SECTION: Controls ===
        self._create_controls(main_frame)
        
        # === STATUS BAR ===
        self._create_status_bar(main_frame)
    
    def _create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg=Config.COLORS['surface'], relief=tk.FLAT)
        header_frame.pack(fill=tk.X, pady=5)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text=f"🤖 {Config.ASSISTANT_NAME}",
            font=(Config.FONT_FAMILY, Config.FONT_SIZE_TITLE, 'bold'),
            fg=Config.COLORS['accent'],
            bg=Config.COLORS['surface']
        )
        title_label.pack(pady=15)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Your Friendly AI Assistant • Ready to Help! 💙",
            font=(Config.FONT_FAMILY, Config.FONT_SIZE_NORMAL),
            fg=Config.COLORS['text_dim'],
            bg=Config.COLORS['surface']
        )
        subtitle_label.pack(pady=5, padx=10, side=tk.BOTTOM)
    
    def _create_animation_area(self, parent):
        """Create animation canvas area"""
        animation_frame = tk.Frame(parent, bg=Config.COLORS['surface'])
        animation_frame.pack(fill=tk.BOTH, pady=10)
        
        # Canvas for animations
        self.animation_canvas = Canvas(
            animation_frame,
            bg=Config.COLORS['surface'],
            height=Config.WAVEFORM_HEIGHT + 40,
            highlightthickness=0
        )
        self.animation_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize animation manager
        self.animation_manager = AnimationManager(self.animation_canvas)
        self.animation_manager.start_pulse()  # Start with idle animation
    
    def _create_chat_area(self, parent):
        """Create chat display area"""
        chat_frame = tk.Frame(parent, bg=Config.COLORS['surface'])
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Label
        chat_label = tk.Label(
            chat_frame,
            text="💬 Conversation",
            font=(Config.FONT_FAMILY, Config.FONT_SIZE_NORMAL, 'bold'),
            fg=Config.COLORS['text'],
            bg=Config.COLORS['surface'],
            anchor=tk.W
        )
        chat_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Chat display (scrolled text)
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=(Config.FONT_FAMILY, Config.FONT_SIZE_NORMAL),
            bg=Config.COLORS['background'],
            fg=Config.COLORS['text'],
            insertbackground=Config.COLORS['text'],
            relief=tk.FLAT,
            padx=15,
            pady=10,
            height=12
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure text tags for styling
        self.chat_display.tag_config('user', foreground=Config.COLORS['listening'], font=(Config.FONT_FAMILY, Config.FONT_SIZE_NORMAL, 'bold'))
        self.chat_display.tag_config('assistant', foreground=Config.COLORS['accent'], font=(Config.FONT_FAMILY, Config.FONT_SIZE_NORMAL, 'bold'))
        self.chat_display.tag_config('system', foreground=Config.COLORS['text_dim'], font=(Config.FONT_FAMILY, Config.FONT_SIZE_NORMAL, 'italic'))
        self.chat_display.tag_config('error', foreground=Config.COLORS['error'])
        
        # Make read-only
        self.chat_display.config(state=tk.DISABLED)
    
    def _create_controls(self, parent):
        """Create control buttons"""
        control_frame = tk.Frame(parent, bg=Config.COLORS['surface'])
        control_frame.pack(fill=tk.X, pady=5)
        
        # Button style configuration
        button_config = {
            'font': (Config.FONT_FAMILY, Config.FONT_SIZE_LARGE, 'bold'),
            'relief': tk.FLAT,
            'cursor': 'hand2',
            'padx': 30,
            'pady': 12,
            'borderwidth': 0
        }
        
        # Speak button
        self.speak_button = tk.Button(
            control_frame,
            text="🎤 Speak",
            bg=Config.COLORS['success'],
            fg='white',
            activebackground=Config.COLORS['listening'],
            command=self._handle_speak,
            **button_config
        )
        self.speak_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Stop button
        self.stop_button = tk.Button(
            control_frame,
            text="⏹️ Stop",
            bg=Config.COLORS['error'],
            fg='white',
            activebackground='#C0392B',
            command=self._handle_stop,
            state=tk.DISABLED,
            **button_config
        )
        self.stop_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Clear button
        clear_button = tk.Button(
            control_frame,
            text="🗑️ Clear",
            bg=Config.COLORS['warning'],
            fg='white',
            activebackground='#E67E22',
            command=self._handle_clear,
            **button_config
        )
        clear_button.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
    
    def _create_status_bar(self, parent):
        """Create status bar"""
        status_frame = tk.Frame(parent, bg=Config.COLORS['surface'], relief=tk.FLAT)
        status_frame.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            status_frame,
            text="🟢 Ready",
            font=(Config.FONT_FAMILY, Config.FONT_SIZE_NORMAL),
            fg=Config.COLORS['text_dim'],
            bg=Config.COLORS['surface'],
            anchor=tk.W,
            padx=10,
            pady=8
        )
        self.status_label.pack(fill=tk.X)
    
    # ==================== EVENT HANDLERS ====================
    
    def _handle_speak(self):
        """Handle speak button click"""
        if self.on_speak_button:
            self.on_speak_button()
    
    def _handle_stop(self):
        """Handle stop button click"""
        if self.on_stop_button:
            self.on_stop_button()
    
    def _handle_clear(self):
        """Handle clear button click"""
        if self.on_clear_button:
            self.on_clear_button()
        else:
            self.clear_chat()
    
    # ==================== PUBLIC METHODS ====================
    
    def add_message(self, role: str, message: str):
        """
        Add message to chat display
        
        Args:
            role: 'user', 'assistant', 'system', or 'error'
            message: Message text
        """
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime('%H:%M')
        
        # Format message based on role
        if role == 'user':
            prefix = f"[{timestamp}] You: "
            self.chat_display.insert(tk.END, prefix, 'user')
        elif role == 'assistant':
            prefix = f"[{timestamp}] {Config.ASSISTANT_NAME}: "
            self.chat_display.insert(tk.END, prefix, 'assistant')
        elif role == 'system':
            prefix = f"[{timestamp}] System: "
            self.chat_display.insert(tk.END, prefix, 'system')
        elif role == 'error':
            prefix = f"[{timestamp}] Error: "
            self.chat_display.insert(tk.END, prefix, 'error')
        
        # Add message content
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Auto-scroll to bottom
        self.chat_display.see(tk.END)
        
        # Make read-only again
        self.chat_display.config(state=tk.DISABLED)
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_message('system', 'Chat cleared')
    
    def set_status(self, status: str, color: str = None):
        """
        Update status bar
        
        Args:
            status: Status text
            color: Optional color override
        """
        if color:
            self.status_label.config(text=status, fg=color)
        else:
            self.status_label.config(text=status)
    
    def set_buttons_enabled(self, speak: bool, stop: bool):
        """
        Enable/disable buttons
        
        Args:
            speak: Enable speak button
            stop: Enable stop button
        """
        self.speak_button.config(state=tk.NORMAL if speak else tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL if stop else tk.DISABLED)
    
    def start_animation(self, animation_type: str):
        """
        Start specific animation
        
        Args:
            animation_type: 'idle', 'listening', 'thinking', 'speaking'
        """
        if self.animation_manager:
            self.animation_manager.switch_animation(animation_type)
    
    def show_greeting(self):
        """Show welcome greeting"""
        from config import get_greeting
        greeting = get_greeting()
        self.add_message('assistant', greeting)
    
    def cleanup(self):
        """Clean up UI resources"""
        if self.animation_manager:
            self.animation_manager.cleanup()
        print("✓ UI cleaned up")


# ==================== TESTING ====================

if __name__ == '__main__':
    """Test UI Manager"""
    
    def test_speak():
        ui.set_status("🎤 Listening...", Config.COLORS['listening'])
        ui.set_buttons_enabled(False, True)
        ui.start_animation('listening')
        ui.add_message('system', 'Speak button clicked (test mode)')
        
        # Simulate response after 2 seconds
        root.after(2000, test_response)
    
    def test_response():
        ui.add_message('user', 'This is a test message from the user')
        ui.set_status("🤖 Thinking...", Config.COLORS['thinking'])
        ui.start_animation('thinking')
        
        # Simulate AI response
        root.after(2000, test_speak_response)
    
    def test_speak_response():
        ui.add_message('assistant', 'This is a test response from Pipoo! How can I help you today? 😊')
        ui.set_status("💬 Speaking...", Config.COLORS['speaking'])
        ui.start_animation('speaking')
        
        # Back to idle
        root.after(2000, test_idle)
    
    def test_idle():
        ui.set_status("🟢 Ready", Config.COLORS['success'])
        ui.set_buttons_enabled(True, False)
        ui.start_animation('idle')
    
    def test_stop():
        ui.set_status("⏹️ Stopped", Config.COLORS['warning'])
        ui.set_buttons_enabled(True, False)
        ui.start_animation('idle')
        ui.add_message('system', 'Stop button clicked (test mode)')
    
    # Create window
    root = tk.Tk()
    
    # Create UI
    ui = UIManager(root)
    
    # Set callbacks
    ui.on_speak_button = test_speak
    ui.on_stop_button = test_stop
    
    # Show greeting
    ui.show_greeting()
    ui.add_message('system', 'UI Test Mode - Click buttons to test functionality')
    
    print("="*60)
    print("UI Manager Test")
    print("Click the Speak button to see animations")
    print("="*60)
    
    # Run
    root.mainloop()