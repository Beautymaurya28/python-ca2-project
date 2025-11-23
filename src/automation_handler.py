"""
Pipoo Desktop Assistant - Automation Handler
Handles system commands, app launching, web browsing, notes, and more
"""

import os
import sys
import webbrowser
import subprocess
import platform
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import re

# Import reminder notifier
try:
    from reminder_notifier import ReminderNotifier
    REMINDER_NOTIFIER_AVAILABLE = True
except ImportError:
    REMINDER_NOTIFIER_AVAILABLE = False
    print("⚠️ reminder_notifier not found - using simple reminder storage")


class AutomationHandler:
    """
    Handles automation commands for Pipoo:
    - Opening applications
    - Web browsing
    - File management
    - Notes and reminders
    - System controls
    """
    
    def __init__(self):
        """Initialize automation handler"""
        self.system = platform.system()  # Windows, Linux, Darwin (macOS)
        self.notes_file = Path.home() / 'pipoo_notes.json'
        self.reminders_file = Path.home() / 'pipoo_reminders.json'
        
        # Load notes and reminders
        self.notes = self._load_notes()
        self.reminders = self._load_reminders()
        
        print("✓ Automation handler initialized")
    
    # ==================== COMMAND DETECTION ====================
    
    def detect_and_execute(self, text: str) -> tuple[bool, str]:
        """
        Detect if text contains a command and execute it
        
        Args:
            text: User input text
            
        Returns:
            (was_command: bool, response: str)
        """
        text_lower = text.lower().strip()
        
        # Check for various command patterns
        
        # Open applications
        if any(word in text_lower for word in ['open', 'launch', 'start']):
            return self._handle_open_command(text_lower)
        
        # Web search
        if 'search' in text_lower or 'google' in text_lower:
            return self._handle_search_command(text_lower)
        
        # Play music/video
        if 'play' in text_lower:
            return self._handle_play_command(text_lower)
        
        # Notes
        if 'note' in text_lower or 'write' in text_lower:
            return self._handle_note_command(text_lower)
        
        # Reminders
        if 'remind' in text_lower or 'reminder' in text_lower:
            return self._handle_reminder_command(text_lower)
        
        # System commands
        if any(word in text_lower for word in ['volume', 'brightness', 'wifi', 'bluetooth']):
            return self._handle_system_command(text_lower)
        
        # File/folder operations
        if 'folder' in text_lower or 'directory' in text_lower:
            return self._handle_folder_command(text_lower)
        
        # Time/date
        if any(word in text_lower for word in ['time', 'date', 'day']):
            return self._handle_time_command(text_lower)
        
        # Not a command
        return False, ""
    
    # ==================== OPEN APPLICATIONS ====================
    
    def _handle_open_command(self, text: str) -> tuple[bool, str]:
        """Handle opening applications"""
        
        # Common applications mapping
        apps = {
            'chrome': ['chrome', 'google chrome', 'browser'],
            'firefox': ['firefox', 'mozilla'],
            'edge': ['edge', 'microsoft edge'],
            'notepad': ['notepad', 'text editor'],
            'calculator': ['calculator', 'calc'],
            'paint': ['paint', 'mspaint'],
            'explorer': ['explorer', 'file explorer', 'files'],
            'cmd': ['cmd', 'command prompt', 'terminal'],
            'youtube': ['youtube'],
            'gmail': ['gmail', 'email', 'mail'],
            'spotify': ['spotify', 'music'],
            'discord': ['discord'],
            'vscode': ['vscode', 'visual studio code', 'code'],
            'word': ['word', 'microsoft word'],
            'excel': ['excel', 'microsoft excel'],
            'powerpoint': ['powerpoint', 'ppt'],
        }
        
        # Check which app to open
        for app_name, keywords in apps.items():
            if any(keyword in text for keyword in keywords):
                success, message = self._open_application(app_name)
                return True, message
        
        return False, ""
    
    def _open_application(self, app_name: str) -> tuple[bool, str]:
        """
        Open specific application
        
        Args:
            app_name: Name of application to open
            
        Returns:
            (success: bool, message: str)
        """
        try:
            if app_name == 'youtube':
                webbrowser.open('https://www.youtube.com')
                return True, "🎥 Opening YouTube for you!"
            
            elif app_name == 'gmail':
                webbrowser.open('https://mail.google.com')
                return True, "📧 Opening Gmail!"
            
            elif app_name == 'chrome':
                if self.system == 'Windows':
                    os.startfile('chrome')
                elif self.system == 'Darwin':  # macOS
                    subprocess.Popen(['open', '-a', 'Google Chrome'])
                else:  # Linux
                    subprocess.Popen(['google-chrome'])
                return True, "🌐 Opening Chrome browser!"
            
            elif app_name == 'firefox':
                if self.system == 'Windows':
                    subprocess.Popen(['firefox'])
                elif self.system == 'Darwin':
                    subprocess.Popen(['open', '-a', 'Firefox'])
                else:
                    subprocess.Popen(['firefox'])
                return True, "🦊 Opening Firefox!"
            
            elif app_name == 'notepad':
                if self.system == 'Windows':
                    os.startfile('notepad')
                else:
                    subprocess.Popen(['gedit'])  # Linux alternative
                return True, "📝 Opening Notepad!"
            
            elif app_name == 'calculator':
                if self.system == 'Windows':
                    os.startfile('calc')
                elif self.system == 'Darwin':
                    subprocess.Popen(['open', '-a', 'Calculator'])
                else:
                    subprocess.Popen(['gnome-calculator'])
                return True, "🔢 Opening Calculator!"
            
            elif app_name == 'explorer':
                if self.system == 'Windows':
                    os.startfile('explorer')
                elif self.system == 'Darwin':
                    subprocess.Popen(['open', '.'])
                else:
                    subprocess.Popen(['nautilus'])
                return True, "📁 Opening File Explorer!"
            
            elif app_name == 'cmd':
                if self.system == 'Windows':
                    os.startfile('cmd')
                elif self.system == 'Darwin':
                    subprocess.Popen(['open', '-a', 'Terminal'])
                else:
                    subprocess.Popen(['gnome-terminal'])
                return True, "💻 Opening Terminal!"
            
            elif app_name == 'paint':
                if self.system == 'Windows':
                    os.startfile('mspaint')
                return True, "🎨 Opening Paint!"
            
            elif app_name == 'spotify':
                if self.system == 'Windows':
                    subprocess.Popen(['spotify'])
                elif self.system == 'Darwin':
                    subprocess.Popen(['open', '-a', 'Spotify'])
                else:
                    subprocess.Popen(['spotify'])
                return True, "🎵 Opening Spotify!"
            
            elif app_name == 'vscode':
                subprocess.Popen(['code'])
                return True, "💻 Opening VS Code!"
            
            else:
                return False, f"I don't know how to open {app_name} yet."
                
        except Exception as e:
            return False, f"❌ Couldn't open {app_name}. Make sure it's installed!"
    
    # ==================== WEB SEARCH ====================
    
    def _handle_search_command(self, text: str) -> tuple[bool, str]:
        """Handle web search commands"""
        
        # Extract search query
        search_patterns = [
            r'search (?:for |about )?(.+)',
            r'google (.+)',
            r'look up (.+)',
            r'find (.+)',
        ]
        
        query = None
        for pattern in search_patterns:
            match = re.search(pattern, text)
            if match:
                query = match.group(1)
                break
        
        if query:
            # Remove common endings
            query = query.replace(' on google', '').replace(' on the internet', '').strip()
            
            # Open Google search
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            
            return True, f"🔍 Searching for '{query}' on Google!"
        
        return False, ""
    
    # ==================== PLAY MEDIA ====================
    
    def _handle_play_command(self, text: str) -> tuple[bool, str]:
        """Handle play music/video commands"""
        
        # Extract what to play
        play_patterns = [
            r'play (.+?) on youtube',
            r'play (.+?) on spotify',
            r'play (.+)',
        ]
        
        query = None
        platform_choice = 'youtube'  # default
        
        for pattern in play_patterns:
            match = re.search(pattern, text)
            if match:
                query = match.group(1)
                if 'spotify' in pattern:
                    platform_choice = 'spotify'
                break
        
        if query:
            if platform_choice == 'youtube':
                search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                return True, f"🎵 Searching for '{query}' on YouTube!"
            elif platform_choice == 'spotify':
                search_url = f"https://open.spotify.com/search/{query.replace(' ', '%20')}"
                webbrowser.open(search_url)
                return True, f"🎵 Searching for '{query}' on Spotify!"
        
        return False, ""
    
    # ==================== NOTES ====================
    
    def _handle_note_command(self, text: str) -> tuple[bool, str]:
        """Handle note creation and retrieval"""
        
        # Delete a specific note
        if 'delete' in text or 'remove' in text:
            delete_patterns = [
                r'delete note (?:number )?(\d+)',
                r'remove note (?:number )?(\d+)',
                r'delete (?:the )?(\d+)(?:st|nd|rd|th)? note',
            ]
            
            for pattern in delete_patterns:
                match = re.search(pattern, text)
                if match:
                    note_num = int(match.group(1))
                    if 1 <= note_num <= len(self.notes):
                        deleted_note = self.notes.pop(note_num - 1)
                        self._save_notes()
                        return True, f"🗑️ Deleted note: '{deleted_note['content']}'"
                    else:
                        return True, f"❌ Note {note_num} doesn't exist. You have {len(self.notes)} notes."
        
        # Clear all notes
        if 'clear' in text or 'delete all' in text:
            if self.notes:
                count = len(self.notes)
                self.notes = []
                self._save_notes()
                return True, f"🗑️ Cleared all {count} notes!"
            else:
                return True, "📝 You don't have any notes to clear."
        
        # Show notes
        if 'show' in text or 'read' in text or 'list' in text or 'display' in text:
            if not self.notes:
                return True, "📝 You don't have any notes yet! Say 'create a note' to make one."
            
            notes_text = f"📝 Your Notes ({len(self.notes)} total):\n\n"
            for i, note in enumerate(self.notes, 1):
                timestamp = note.get('timestamp', 'Unknown time')
                # Format timestamp nicely
                try:
                    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    time_str = dt.strftime('%b %d, %I:%M %p')
                except:
                    time_str = timestamp
                
                content = note.get('content', '')
                notes_text += f"{i}. {content}\n   📅 {time_str}\n\n"
            
            return True, notes_text.strip()
        
        # Create note - more flexible patterns
        note_patterns = [
            r'(?:create|make|write|take|add|save) (?:a |an |new )?note (?:saying |that says |about )?(.+)',
            r'note (?:down )?(?:that )?(.+)',
            r'remember (?:that )?(.+)',
            r'write (?:down )?(.+)',
        ]
        
        content = None
        for pattern in note_patterns:
            match = re.search(pattern, text)
            if match:
                content = match.group(1).strip()
                # Clean up common endings
                content = content.replace(' please', '').replace(' thanks', '')
                break
        
        if content and len(content) > 3:  # At least 3 characters
            note = {
                'content': content,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'id': len(self.notes) + 1
            }
            self.notes.append(note)
            self._save_notes()
            
            return True, f"✅ Note saved! You now have {len(self.notes)} note(s).\n💭 '{content}'"
        
        return False, ""
    
    def _load_notes(self) -> List[Dict]:
        """Load notes from file"""
        if self.notes_file.exists():
            try:
                with open(self.notes_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_notes(self):
        """Save notes to file"""
        with open(self.notes_file, 'w') as f:
            json.dump(self.notes, f, indent=2)
    
    # ==================== REMINDERS ====================
    
    def _handle_reminder_command(self, text: str) -> tuple[bool, str]:
        """Handle reminder creation and management"""
        
        # Delete a specific reminder
        if 'delete' in text or 'remove' in text or 'cancel' in text:
            delete_patterns = [
                r'delete reminder (?:number )?(\d+)',
                r'remove reminder (?:number )?(\d+)',
                r'cancel reminder (?:number )?(\d+)',
            ]
            
            for pattern in delete_patterns:
                match = re.search(pattern, text)
                if match:
                    reminder_num = int(match.group(1))
                    if 1 <= reminder_num <= len(self.reminders):
                        deleted = self.reminders.pop(reminder_num - 1)
                        self._save_reminders()
                        return True, f"🗑️ Deleted reminder: '{deleted['content']}'"
                    else:
                        return True, f"❌ Reminder {reminder_num} doesn't exist."
        
        # Clear all reminders
        if 'clear all' in text or 'delete all' in text:
            if self.reminders:
                count = len(self.reminders)
                self.reminders = []
                self._save_reminders()
                return True, f"🗑️ Cleared all {count} reminders!"
            else:
                return True, "⏰ You don't have any reminders to clear."
        
        # Show reminders
        if 'show' in text or 'list' in text or 'display' in text or 'view' in text:
            if not self.reminders:
                return True, "⏰ You don't have any reminders yet! Say 'set a reminder' to create one."
            
            reminders_text = f"⏰ Your Reminders ({len(self.reminders)} total):\n\n"
            for i, reminder in enumerate(self.reminders, 1):
                content = reminder.get('content', '')
                when = reminder.get('when', 'Unknown time')
                created = reminder.get('created', '')
                
                # Format creation time
                try:
                    dt = datetime.strptime(created, '%Y-%m-%d %H:%M:%S')
                    created_str = dt.strftime('%b %d, %I:%M %p')
                except:
                    created_str = created
                
                reminders_text += f"{i}. {content}\n   ⏰ Remind: {when}\n   📅 Set: {created_str}\n\n"
            
            return True, reminders_text.strip()
        
        # Create reminder - Enhanced patterns
        reminder_patterns = [
            r'(?:remind me|set (?:a )?reminder|reminder) (?:to )?(.+?) (?:in|at|on) (.+)',
            r'(?:remind|reminder) (?:me )?(?:to )?(.+?) (?:in|at|on) (.+)',
        ]
        
        for pattern in reminder_patterns:
            match = re.search(pattern, text)
            if match:
                content = match.group(1).strip()
                when = match.group(2).strip()
                
                # Clean up content
                content = content.replace(' please', '').replace(' thanks', '')
                
                # Parse time if possible
                reminder_time = self._parse_reminder_time(when)
                
                reminder = {
                    'content': content,
                    'when': when,
                    'reminder_time': reminder_time,
                    'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'id': len(self.reminders) + 1
                }
                self.reminders.append(reminder)
                self._save_reminders()
                
                response = f"⏰ Reminder set! You now have {len(self.reminders)} reminder(s).\n"
                response += f"📌 '{content}' - {when}"
                if reminder_time:
                    response += f"\n🕐 That's {reminder_time}"
                
                return True, response
        
        return False, ""
    
    def _parse_reminder_time(self, when: str) -> Optional[str]:
        """Parse reminder time into human-readable format"""
        try:
            when_lower = when.lower()
            
            # Handle relative times
            if 'minute' in when_lower:
                match = re.search(r'(\d+)\s*minute', when_lower)
                if match:
                    minutes = int(match.group(1))
                    future_time = datetime.now() + timedelta(minutes=minutes)
                    return future_time.strftime('%I:%M %p today')
            
            elif 'hour' in when_lower:
                match = re.search(r'(\d+)\s*hour', when_lower)
                if match:
                    hours = int(match.group(1))
                    future_time = datetime.now() + timedelta(hours=hours)
                    return future_time.strftime('%I:%M %p today')
            
            elif 'day' in when_lower:
                match = re.search(r'(\d+)\s*day', when_lower)
                if match:
                    days = int(match.group(1))
                    future_time = datetime.now() + timedelta(days=days)
                    return future_time.strftime('%b %d at %I:%M %p')
            
            # Handle specific times
            elif 'tomorrow' in when_lower:
                tomorrow = datetime.now() + timedelta(days=1)
                return tomorrow.strftime('%b %d (tomorrow)')
            
            elif any(day in when_lower for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']):
                return when  # Return as is for day names
            
        except:
            pass
        
        return None
    
    def _load_reminders(self) -> List[Dict]:
        """Load reminders from file"""
        if self.reminders_file.exists():
            try:
                with open(self.reminders_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_reminders(self):
        """Save reminders to file"""
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f, indent=2)
    
    # ==================== SYSTEM COMMANDS ====================
    
    def _handle_system_command(self, text: str) -> tuple[bool, str]:
        """Handle system control commands"""
        
        # Volume control
        if 'volume' in text:
            if 'up' in text or 'increase' in text:
                return True, "🔊 Volume increased! (Feature requires system integration)"
            elif 'down' in text or 'decrease' in text:
                return True, "🔉 Volume decreased! (Feature requires system integration)"
            elif 'mute' in text:
                return True, "🔇 Volume muted! (Feature requires system integration)"
        
        return False, ""
    
    # ==================== FOLDER OPERATIONS ====================
    
    def _handle_folder_command(self, text: str) -> tuple[bool, str]:
        """Handle folder/directory operations"""
        
        if 'open' in text:
            # Open common folders
            if 'documents' in text:
                docs_path = Path.home() / 'Documents'
                self._open_folder(docs_path)
                return True, "📁 Opening Documents folder!"
            
            elif 'downloads' in text:
                downloads_path = Path.home() / 'Downloads'
                self._open_folder(downloads_path)
                return True, "📥 Opening Downloads folder!"
            
            elif 'desktop' in text:
                desktop_path = Path.home() / 'Desktop'
                self._open_folder(desktop_path)
                return True, "🖥️ Opening Desktop!"
        
        return False, ""
    
    def _open_folder(self, path: Path):
        """Open a folder in file explorer"""
        if self.system == 'Windows':
            os.startfile(path)
        elif self.system == 'Darwin':
            subprocess.Popen(['open', str(path)])
        else:
            subprocess.Popen(['xdg-open', str(path)])
    
    # ==================== TIME/DATE ====================
    
    def _handle_time_command(self, text: str) -> tuple[bool, str]:
        """Handle time and date queries"""
        
        now = datetime.now()
        
        if 'time' in text:
            current_time = now.strftime('%I:%M %p')
            return True, f"🕐 The current time is {current_time}"
        
        elif 'date' in text:
            current_date = now.strftime('%A, %B %d, %Y')
            return True, f"📅 Today is {current_date}"
        
        elif 'day' in text:
            day_name = now.strftime('%A')
            return True, f"📆 Today is {day_name}"
        
        return False, ""


# ==================== TESTING ====================

if __name__ == '__main__':
    """Test automation handler"""
    
    print("="*60)
    print("Pipoo Automation Handler Test")
    print("="*60)
    
    automation = AutomationHandler()
    
    # Test commands
    test_commands = [
        "open YouTube",
        "search for cute cats",
        "play some relaxing music",
        "create a note saying buy groceries",
        "show my notes",
        "what time is it",
        "open chrome",
        "remind me to call mom in 2 hours",
    ]
    
    print("\nTesting commands:\n")
    
    for command in test_commands:
        print(f"Command: '{command}'")
        is_command, response = automation.detect_and_execute(command)
        if is_command:
            print(f"✓ Response: {response}")
        else:
            print(f"✗ Not recognized as command")
        print()
    
    print("="*60)
    print("Test complete!")
    print("="*60)