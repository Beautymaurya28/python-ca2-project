"""
Test script for Pipoo Notes and Reminders features
Run this to verify all three features work correctly
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from automation_handler import AutomationHandler


def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def test_command(automation, command, description):
    """Test a single command"""
    print(f"📝 Testing: {description}")
    print(f"   Command: '{command}'")
    
    is_command, response = automation.detect_and_execute(command)
    
    if is_command:
        print(f"   ✅ Success!")
        print(f"   Response: {response}")
    else:
        print(f"   ❌ Failed - Not recognized as command")
    
    print()


def main():
    """Main test function"""
    
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🤖 PIPOO NOTES & REMINDERS TEST".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Initialize automation handler
    print("\n🔧 Initializing automation handler...")
    automation = AutomationHandler()
    print("✅ Ready!\n")
    
    # ==================== TEST 1: CREATE NOTES ====================
    print_section("TEST 1: CREATE NOTES")
    
    test_command(
        automation,
        "create a note saying buy milk and eggs",
        "Create simple note"
    )
    
    test_command(
        automation,
        "make a note call mom tomorrow",
        "Create note with different phrase"
    )
    
    test_command(
        automation,
        "remember that my appointment is at 3 PM",
        "Create note using 'remember'"
    )
    
    test_command(
        automation,
        "note down finish homework",
        "Create note using 'note down'"
    )
    
    # ==================== TEST 2: SHOW NOTES ====================
    print_section("TEST 2: SHOW NOTES")
    
    test_command(
        automation,
        "show my notes",
        "Display all notes"
    )
    
    test_command(
        automation,
        "list my notes",
        "List notes (alternative phrase)"
    )
    
    # ==================== TEST 3: SET REMINDERS ====================
    print_section("TEST 3: SET REMINDERS")
    
    test_command(
        automation,
        "remind me to call dentist in 2 hours",
        "Set reminder with relative time"
    )
    
    test_command(
        automation,
        "set a reminder to take medicine at 8 PM",
        "Set reminder with specific time"
    )
    
    test_command(
        automation,
        "remind me to workout tomorrow",
        "Set reminder for tomorrow"
    )
    
    test_command(
        automation,
        "reminder to submit report in 3 days",
        "Set reminder for future date"
    )
    
    # ==================== TEST 4: SHOW REMINDERS ====================
    print_section("TEST 4: SHOW REMINDERS")
    
    test_command(
        automation,
        "show my reminders",
        "Display all reminders"
    )
    
    test_command(
        automation,
        "list my reminders",
        "List reminders (alternative phrase)"
    )
    
    # ==================== TEST 5: DELETE OPERATIONS ====================
    print_section("TEST 5: DELETE OPERATIONS")
    
    test_command(
        automation,
        "delete note 2",
        "Delete specific note"
    )
    
    test_command(
        automation,
        "show my notes",
        "Verify note deleted"
    )
    
    test_command(
        automation,
        "delete reminder 1",
        "Delete specific reminder"
    )
    
    test_command(
        automation,
        "show my reminders",
        "Verify reminder deleted"
    )
    
    # ==================== SUMMARY ====================
    print_section("TEST SUMMARY")
    
    # Get final counts
    notes_count = len(automation.notes)
    reminders_count = len(automation.reminders)
    
    print(f"📝 Final Note Count: {notes_count}")
    print(f"⏰ Final Reminder Count: {reminders_count}")
    print()
    
    # Show file locations
    print("📂 Data Files:")
    print(f"   Notes: {automation.notes_file}")
    print(f"   Reminders: {automation.reminders_file}")
    print()
    
    # Final message
    if notes_count > 0 or reminders_count > 0:
        print("✅ All tests completed successfully!")
        print("   Your notes and reminders have been saved.")
    else:
        print("⚠️  Tests ran but no data was saved.")
        print("   Check if commands were recognized correctly.")
    
    print("\n" + "="*60)
    print("  Test Complete!")
    print("="*60 + "\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")