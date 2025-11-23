"""
Pipoo Desktop Assistant - Animation Manager (FIXED - No Color Errors)
Handles all UI animations including waveforms, pulses, and transitions
"""

import tkinter as tk
from tkinter import Canvas
import math
import random
from typing import Optional, Tuple, List
from config import Config


class AnimationManager:
    """
    Manages all animations for Pipoo UI:
    - Waveform animation (listening)
    - Pulse animation (idle)
    - Typing animation (thinking)
    - Smooth transitions
    """
    
    def __init__(self, canvas: Canvas):
        """
        Initialize animation manager
        
        Args:
            canvas: Tkinter Canvas widget for drawing animations
        """
        self.canvas = canvas
        self.is_running = False
        self.current_animation = 'idle'
        self.animation_objects = []
        
        # Animation state
        self.frame = 0
        self.wave_heights = [0] * Config.WAVEFORM_BARS
        self.pulse_index = 0
        self.typing_index = 0
        
        # Animation IDs for cleanup
        self.animation_id = None
        
        print("✓ Animation manager initialized")
    
    # ==================== WAVEFORM ANIMATION ====================
    
    def start_waveform(self):
        """Start waveform animation (for listening state)"""
        self.current_animation = 'waveform'
        self.is_running = True
        self._animate_waveform()
    
    def _animate_waveform(self):
        """Animate waveform bars"""
        if not self.is_running or self.current_animation != 'waveform':
            return
        
        # Clear canvas
        self.canvas.delete('all')
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            # Canvas not ready, try again
            self.animation_id = self.canvas.after(50, self._animate_waveform)
            return
        
        # Calculate bar properties
        bar_width = width / Config.WAVEFORM_BARS
        max_height = height * 0.8
        
        # Update wave heights with smooth random movement
        for i in range(Config.WAVEFORM_BARS):
            target = random.uniform(0.2, 1.0) * max_height
            self.wave_heights[i] += (target - self.wave_heights[i]) * 0.15
        
        # Draw bars with FIXED colors
        for i, bar_height in enumerate(self.wave_heights):
            x1 = i * bar_width + bar_width * 0.1
            x2 = (i + 1) * bar_width - bar_width * 0.1
            y1 = (height - bar_height) / 2
            y2 = (height + bar_height) / 2
            
            # Use predefined colors - no dynamic calculation
            colors = ['#3498DB', '#5DADE2', '#85C1E9', '#AED6F1']
            color = colors[i % len(colors)]
            
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline='',
                tags='waveform'
            )
        
        self.frame += 1
        self.animation_id = self.canvas.after(Config.WAVEFORM_UPDATE_MS, self._animate_waveform)
    
    # ==================== PULSE ANIMATION ====================
    
    def start_pulse(self):
        """Start pulse animation (for idle state)"""
        self.current_animation = 'pulse'
        self.is_running = True
        self.pulse_index = 0
        self._animate_pulse()
    
    def _animate_pulse(self):
        """Animate pulsing circle"""
        if not self.is_running or self.current_animation != 'pulse':
            return
        
        # Clear canvas
        self.canvas.delete('all')
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            self.animation_id = self.canvas.after(50, self._animate_pulse)
            return
        
        # Calculate circle properties
        center_x = width / 2
        center_y = height / 2
        
        # Pulse size based on sine wave
        pulse_phase = (self.frame / 30) * math.pi * 2
        size_multiplier = 0.7 + 0.3 * math.sin(pulse_phase)
        radius = min(width, height) * 0.3 * size_multiplier
        
        # Draw outer glow rings with FIXED colors
        glow_colors = ['#5DADE2', '#7FB3D5', '#A9CCE3']
        for i in range(3):
            glow_radius = radius + (i + 1) * 10
            color = glow_colors[i]
            
            self.canvas.create_oval(
                center_x - glow_radius, center_y - glow_radius,
                center_x + glow_radius, center_y + glow_radius,
                fill=color,
                outline='',
                tags='pulse'
            )
        
        # Draw main circle
        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=Config.COLORS['primary'],
            outline=Config.COLORS['listening'],
            width=3,
            tags='pulse'
        )
        
        # Draw cute robot face emoji in center
        emoji_size = int(radius * 0.8)
        self.canvas.create_text(
            center_x, center_y,
            text='🤖',
            font=('Arial', emoji_size),
            tags='pulse'
        )
        
        self.frame += 1
        self.animation_id = self.canvas.after(Config.PULSE_SPEED_MS, self._animate_pulse)
    
    # ==================== TYPING ANIMATION ====================
    
    def start_typing(self):
        """Start typing animation (for thinking state)"""
        self.current_animation = 'typing'
        self.is_running = True
        self.typing_index = 0
        self._animate_typing()
    
    def _animate_typing(self):
        """Animate typing dots"""
        if not self.is_running or self.current_animation != 'typing':
            return
        
        # Clear canvas
        self.canvas.delete('all')
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            self.animation_id = self.canvas.after(50, self._animate_typing)
            return
        
        center_x = width / 2
        center_y = height / 2
        
        # Draw robot thinking
        self.canvas.create_text(
            center_x, center_y - 30,
            text='🤖',
            font=('Arial', 50),
            tags='typing'
        )
        
        # Draw thinking bubble
        bubble_text = Config.TYPING_DOTS[self.typing_index % len(Config.TYPING_DOTS)]
        self.canvas.create_text(
            center_x, center_y + 40,
            text=f'💭 {bubble_text}',
            font=(Config.FONT_FAMILY, 20),
            fill=Config.COLORS['text'],
            tags='typing'
        )
        
        self.typing_index += 1
        self.animation_id = self.canvas.after(Config.TYPING_SPEED_MS, self._animate_typing)
    
    # ==================== SPEAKING ANIMATION ====================
    
    def start_speaking(self):
        """Start speaking animation"""
        self.current_animation = 'speaking'
        self.is_running = True
        self._animate_speaking()
    
    def _animate_speaking(self):
        """Animate speaking state"""
        if not self.is_running or self.current_animation != 'speaking':
            return
        
        # Clear canvas
        self.canvas.delete('all')
        
        # Get canvas dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            self.animation_id = self.canvas.after(50, self._animate_speaking)
            return
        
        center_x = width / 2
        center_y = height / 2
        
        # Draw pulsing circle
        pulse_phase = (self.frame / 15) * math.pi * 2
        size_multiplier = 0.8 + 0.2 * math.sin(pulse_phase)
        radius = min(width, height) * 0.25 * size_multiplier
        
        # Glow effect with FIXED colors
        glow_colors = ['#BB8FCE', '#D7BDE2', '#E8DAEF']
        for i in range(3):
            glow_radius = radius + (i + 1) * 15
            color = glow_colors[i]
            
            self.canvas.create_oval(
                center_x - glow_radius, center_y - glow_radius,
                center_x + glow_radius, center_y + glow_radius,
                fill=color,
                outline='',
                tags='speaking'
            )
        
        # Main circle
        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=Config.COLORS['speaking'],
            outline=Config.COLORS['accent'],
            width=3,
            tags='speaking'
        )
        
        # Robot speaking
        self.canvas.create_text(
            center_x, center_y,
            text='🤖',
            font=('Arial', int(radius * 1.2)),
            tags='speaking'
        )
        
        # Sound waves with FIXED colors
        wave_colors = ['#85C1E9', '#AED6F1', '#D6EAF8']
        for i in range(3):
            wave_radius = radius + 40 + i * 20
            color = wave_colors[i]
            
            self.canvas.create_arc(
                center_x - wave_radius, center_y - wave_radius,
                center_x + wave_radius, center_y + wave_radius,
                start=30, extent=120,
                style=tk.ARC,
                outline=color,
                width=3,
                tags='speaking'
            )
        
        self.frame += 1
        self.animation_id = self.canvas.after(50, self._animate_speaking)
    
    # ==================== CONTROL METHODS ====================
    
    def stop(self):
        """Stop current animation"""
        self.is_running = False
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None
        self.canvas.delete('all')
    
    def switch_animation(self, animation_type: str):
        """
        Switch to different animation
        
        Args:
            animation_type: 'idle', 'listening', 'thinking', 'speaking'
        """
        # Map animation types to methods
        animation_map = {
            'idle': self.start_pulse,
            'listening': self.start_waveform,
            'thinking': self.start_typing,
            'speaking': self.start_speaking,
            'pulse': self.start_pulse
        }
        
        # Stop current animation
        self.stop()
        
        # Start new animation
        if animation_type in animation_map:
            animation_map[animation_type]()
        else:
            print(f"⚠️ Unknown animation type: {animation_type}")
            self.start_pulse()
    
    def cleanup(self):
        """Clean up animations"""
        self.stop()
        print("✓ Animations cleaned up")


# ==================== TESTING ====================

if __name__ == '__main__':
    """Test animations in a simple window"""
    
    def test_animation(anim_type):
        """Switch to test animation"""
        print(f"Testing {anim_type} animation...")
        anim_manager.switch_animation(anim_type)
    
    # Create test window
    root = tk.Tk()
    root.title("Pipoo Animation Test")
    root.geometry("600x400")
    root.configure(bg=Config.COLORS['background'])
    
    # Create canvas
    canvas = Canvas(
        root,
        bg=Config.COLORS['background'],
        highlightthickness=0,
        width=600,
        height=300
    )
    canvas.pack(pady=20)
    
    # Create animation manager
    anim_manager = AnimationManager(canvas)
    
    # Control frame
    control_frame = tk.Frame(root, bg=Config.COLORS['background'])
    control_frame.pack(pady=10)
    
    # Test buttons
    animations = ['idle', 'listening', 'thinking', 'speaking']
    for anim in animations:
        btn = tk.Button(
            control_frame,
            text=anim.capitalize(),
            command=lambda a=anim: test_animation(a),
            bg=Config.COLORS['primary'],
            fg=Config.COLORS['text'],
            font=(Config.FONT_FAMILY, 10),
            padx=15,
            pady=5
        )
        btn.pack(side=tk.LEFT, padx=5)
    
    # Start with idle animation
    anim_manager.start_pulse()
    
    # Run
    print("="*60)
    print("Animation Test Window")
    print("Click buttons to test different animations")
    print("="*60)
    
    root.mainloop()