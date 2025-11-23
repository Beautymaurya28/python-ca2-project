"""
Pipoo Desktop Assistant - Reminder Notifier
Actively monitors and triggers reminders at the right time
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Optional, Callable
import re


class ReminderNotifier:
    """
    Active reminder system that monitors and triggers reminders
    """
    
    def __init__(self):
        """Initialize reminder notifier"""
        self.active_reminders = []
        self.is_running = False
        self.monitor_thread = None
        
        # Callbacks
        self.on_reminder_trigger: Optional[Callable] = None
        
        print("✓ Reminder notifier initialized")
    
    def start(self):
        """Start monitoring reminders"""
        if not self.is_running:
            self.is_running = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            print("✓ Reminder monitoring started")
    
    def stop(self):
        """Stop monitoring reminders"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("✓ Reminder monitoring stopped")
    
    def add_reminder(self, content: str, when: str) -> tuple[bool, str, Optional[datetime]]:
        """
        Add a reminder with time parsing
        
        Args:
            content: What to remind
            when: When to remind (e.g., "in 5 minutes", "at 8 PM")
            
        Returns:
            (success: bool, message: str, trigger_time: datetime)
        """
        trigger_time = self._parse_time(when)
        
        if not trigger_time:
            return False, f"⚠️ Couldn't understand the time '{when}'. Try 'in 5 minutes' or 'at 8 PM'", None
        
        # Check if time is in the past
        if trigger_time <= datetime.now():
            return False, "⚠️ That time is in the past! Please set a future time.", None
        
        # Create reminder
        reminder = {
            'content': content,
            'when': when,
            'trigger_time': trigger_time,
            'triggered': False,
            'created': datetime.now()
        }
        
        self.active_reminders.append(reminder)
        
        # Calculate time until reminder
        time_diff = trigger_time - datetime.now()
        seconds = int(time_diff.total_seconds())
        
        # Format response
        time_str = self._format_time_until(seconds)
        trigger_str = trigger_time.strftime('%I:%M %p')
        
        return True, f"⏰ Reminder set! I'll remind you {when}.\n🕐 That's at {trigger_str} ({time_str})", trigger_time
    
    def get_active_reminders(self) -> list:
        """Get list of active (non-triggered) reminders"""
        return [r for r in self.active_reminders if not r['triggered']]
    
    def remove_reminder(self, index: int) -> bool:
        """Remove a reminder by index"""
        active = self.get_active_reminders()
        if 0 <= index < len(active):
            reminder = active[index]
            self.active_reminders.remove(reminder)
            return True
        return False
    
    def clear_all(self):
        """Clear all reminders"""
        self.active_reminders = []
    
    def _monitor_loop(self):
        """Main monitoring loop (runs in background thread)"""
        while self.is_running:
            try:
                now = datetime.now()
                
                # Check each reminder
                for reminder in self.active_reminders:
                    if not reminder['triggered']:
                        trigger_time = reminder['trigger_time']
                        
                        # Check if it's time to trigger (within 2 seconds tolerance)
                        if now >= trigger_time or (trigger_time - now).total_seconds() <= 2:
                            self._trigger_reminder(reminder)
                
                # Sleep for 1 second before next check
                time.sleep(1)
                
            except Exception as e:
                print(f"⚠️ Reminder monitor error: {e}")
                time.sleep(1)
    
    def _trigger_reminder(self, reminder: dict):
        """Trigger a reminder notification"""
        reminder['triggered'] = True
        
        content = reminder['content']
        when = reminder['when']
        
        print(f"\n🔔 REMINDER: {content}")
        print(f"   (Set for: {when})")
        
        # Call callback if set
        if self.on_reminder_trigger:
            self.on_reminder_trigger(content, when)
    
    def _parse_time(self, when: str) -> Optional[datetime]:
        """
        Parse time string into datetime
        
        Args:
            when: Time string like "in 5 minutes", "at 8 PM", "tomorrow"
            
        Returns:
            datetime object or None if parsing failed
        """
        when_lower = when.lower().strip()
        now = datetime.now()
        
        try:
            # "in X minutes/hours/seconds"
            match = re.search(r'in\s+(\d+)\s*(second|minute|hour|day)s?', when_lower)
            if match:
                amount = int(match.group(1))
                unit = match.group(2)
                
                if unit == 'second':
                    return now + timedelta(seconds=amount)
                elif unit == 'minute':
                    return now + timedelta(minutes=amount)
                elif unit == 'hour':
                    return now + timedelta(hours=amount)
                elif unit == 'day':
                    return now + timedelta(days=amount)
            
            # "at HH:MM AM/PM" or "at H PM"
            match = re.search(r'at\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', when_lower)
            if match:
                hour = int(match.group(1))
                minute = int(match.group(2)) if match.group(2) else 0
                am_pm = match.group(3)
                
                # Convert to 24-hour format
                if am_pm:
                    if am_pm == 'pm' and hour != 12:
                        hour += 12
                    elif am_pm == 'am' and hour == 12:
                        hour = 0
                
                # Create target time today
                target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                
                # If time has passed today, set for tomorrow
                if target <= now:
                    target += timedelta(days=1)
                
                return target
            
            # "tomorrow" or "tomorrow at X"
            if 'tomorrow' in when_lower:
                tomorrow = now + timedelta(days=1)
                
                # Check if specific time is mentioned
                match = re.search(r'at\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', when_lower)
                if match:
                    hour = int(match.group(1))
                    minute = int(match.group(2)) if match.group(2) else 0
                    am_pm = match.group(3)
                    
                    if am_pm:
                        if am_pm == 'pm' and hour != 12:
                            hour += 12
                        elif am_pm == 'am' and hour == 12:
                            hour = 0
                    
                    return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
                else:
                    # Tomorrow at same time
                    return tomorrow
            
            # Day names (monday, tuesday, etc.)
            days = {
                'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                'friday': 4, 'saturday': 5, 'sunday': 6
            }
            
            for day_name, day_num in days.items():
                if day_name in when_lower:
                    # Calculate days until target day
                    current_day = now.weekday()
                    days_ahead = day_num - current_day
                    
                    if days_ahead <= 0:  # Target day has passed this week
                        days_ahead += 7
                    
                    target_date = now + timedelta(days=days_ahead)
                    
                    # Check for specific time
                    match = re.search(r'at\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', when_lower)
                    if match:
                        hour = int(match.group(1))
                        minute = int(match.group(2)) if match.group(2) else 0
                        am_pm = match.group(3)
                        
                        if am_pm:
                            if am_pm == 'pm' and hour != 12:
                                hour += 12
                            elif am_pm == 'am' and hour == 12:
                                hour = 0
                        
                        return target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    else:
                        return target_date
            
        except Exception as e:
            print(f"⚠️ Time parsing error: {e}")
        
        return None
    
    def _format_time_until(self, seconds: int) -> str:
        """Format seconds into human-readable time"""
        if seconds < 60:
            return f"in {seconds} seconds"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"in {minutes} minute{'s' if minutes != 1 else ''}"
        elif seconds < 86400:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if minutes > 0:
                return f"in {hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
            else:
                return f"in {hours} hour{'s' if hours != 1 else ''}"
        else:
            days = seconds // 86400
            hours = (seconds % 86400) // 3600
            if hours > 0:
                return f"in {days} day{'s' if days != 1 else ''} and {hours} hour{'s' if hours != 1 else ''}"
            else:
                return f"in {days} day{'s' if days != 1 else ''}"


# ==================== TESTING ====================

if __name__ == '__main__':
    """Test reminder notifier"""
    
    print("="*60)
    print("Pipoo Reminder Notifier Test")
    print("="*60)
    
    def reminder_callback(content, when):
        """Callback when reminder triggers"""
        print(f"\n🔔🔔🔔 REMINDER TRIGGERED! 🔔🔔🔔")
        print(f"📌 {content}")
        print(f"⏰ Was set for: {when}")
        print("="*60)
    
    # Initialize notifier
    notifier = ReminderNotifier()
    notifier.on_reminder_trigger = reminder_callback
    
    # Start monitoring
    notifier.start()
    
    # Test reminders
    print("\n📝 Testing reminders...")
    
    # Test 1: Short reminder (10 seconds)
    success, msg, trigger_time = notifier.add_reminder("Test short reminder", "in 10 seconds")
    print(f"\n1. {msg}")
    
    # Test 2: Medium reminder (30 seconds)
    success, msg, trigger_time = notifier.add_reminder("Test medium reminder", "in 30 seconds")
    print(f"\n2. {msg}")
    
    # Test 3: One minute
    success, msg, trigger_time = notifier.add_reminder("Test one minute reminder", "in 1 minute")
    print(f"\n3. {msg}")
    
    # Show active reminders
    print("\n" + "="*60)
    print("Active Reminders:")
    for i, r in enumerate(notifier.get_active_reminders(), 1):
        time_left = (r['trigger_time'] - datetime.now()).total_seconds()
        print(f"{i}. {r['content']} - {int(time_left)} seconds remaining")
    
    print("\n⏳ Waiting for reminders to trigger...")
    print("(This will take about 1 minute)")
    print("="*60)
    
    # Wait for reminders to trigger
    try:
        time.sleep(70)  # Wait 70 seconds
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    
    # Stop monitoring
    notifier.stop()
    
    print("\n" + "="*60)
    print("Test complete!")
    print("="*60)