# 📝 Pipoo Notes & Reminders - Complete Guide

## 🎯 Three Core Features

Pipoo can now manage your notes and reminders with voice commands!

---

## 📝 **FEATURE 1: CREATE NOTES**

### How to Create Notes:

Say any of these:

```
✅ "Pipoo, create a note saying buy groceries"
✅ "Create a note buy milk and eggs"
✅ "Make a note call mom tomorrow"
✅ "Write a note meeting at 3 PM"
✅ "Take a note password is 12345"
✅ "Remember that my appointment is Tuesday"
✅ "Note down finish homework"
```

### What Happens:
1. Pipoo saves your note with timestamp
2. You get confirmation: "✅ Note saved!"
3. Notes are stored permanently in `pipoo_notes.json`

### Examples:

**Example 1:**
```
You: "Create a note saying buy milk, eggs, and bread"
Pipoo: ✅ Note saved! You now have 1 note(s).
       💭 'buy milk, eggs, and bread'
```

**Example 2:**
```
You: "Remember that my password is stored in vault"
Pipoo: ✅ Note saved! You now have 2 note(s).
       💭 'my password is stored in vault'
```

**Example 3:**
```
You: "Write a note doctor appointment Thursday 2 PM"
Pipoo: ✅ Note saved! You now have 3 note(s).
       💭 'doctor appointment Thursday 2 PM'
```

---

## 📋 **FEATURE 2: SHOW NOTES**

### How to View Your Notes:

Say any of these:

```
✅ "Pipoo, show my notes"
✅ "Show my notes"
✅ "Read my notes"
✅ "List my notes"
✅ "Display my notes"
✅ "What are my notes?"
```

### What You'll See:
- All your notes numbered (1, 2, 3...)
- Each note with its content
- Date and time when you created it
- Total count of notes

### Example Output:

```
You: "Show my notes"
Pipoo: 📝 Your Notes (3 total):

       1. buy milk, eggs, and bread
          📅 Nov 17, 02:30 PM

       2. my password is stored in vault
          📅 Nov 17, 02:31 PM

       3. doctor appointment Thursday 2 PM
          📅 Nov 17, 02:32 PM
```

### If You Have No Notes:

```
You: "Show my notes"
Pipoo: 📝 You don't have any notes yet! Say 'create a note' to make one.
```

---

## ⏰ **FEATURE 3: SET REMINDERS**

### How to Create Reminders:

Say any of these patterns:

```
✅ "Pipoo, remind me to call mom in 2 hours"
✅ "Set a reminder to take medicine at 8 PM"
✅ "Remind me to submit report in 30 minutes"
✅ "Reminder to workout tomorrow"
✅ "Set reminder call dentist on Monday"
✅ "Remind me to buy groceries in 3 days"
```

### Time Formats Supported:

**Relative Times:**
- "in 5 minutes"
- "in 2 hours"
- "in 3 days"

**Specific Times:**
- "at 8 PM"
- "at 3:30 PM"
- "tomorrow"
- "on Monday"
- "on Tuesday at 5 PM"

### Examples:

**Example 1:**
```
You: "Remind me to call mom in 2 hours"
Pipoo: ⏰ Reminder set! You now have 1 reminder(s).
       📌 'call mom' - in 2 hours
       🕐 That's 04:30 PM today
```

**Example 2:**
```
You: "Set a reminder to take medicine at 8 PM"
Pipoo: ⏰ Reminder set! You now have 2 reminder(s).
       📌 'take medicine' - at 8 PM
```

**Example 3:**
```
You: "Remind me to submit report tomorrow"
Pipoo: ⏰ Reminder set! You now have 3 reminder(s).
       📌 'submit report' - tomorrow
       🕐 That's Nov 18 (tomorrow)
```

---

## 📊 **VIEW REMINDERS**

### How to See Your Reminders:

```
✅ "Show my reminders"
✅ "List my reminders"
✅ "Display my reminders"
✅ "View my reminders"
✅ "What are my reminders?"
```

### Example Output:

```
You: "Show my reminders"
Pipoo: ⏰ Your Reminders (3 total):

       1. call mom
          ⏰ Remind: in 2 hours
          📅 Set: Nov 17, 02:30 PM

       2. take medicine
          ⏰ Remind: at 8 PM
          📅 Set: Nov 17, 02:31 PM

       3. submit report
          ⏰ Remind: tomorrow
          📅 Set: Nov 17, 02:32 PM
```

---

## 🗑️ **BONUS: Delete & Clear**

### Delete Specific Note:

```
✅ "Delete note 2"
✅ "Remove note number 3"
✅ "Delete the first note"

Pipoo: 🗑️ Deleted note: 'my password is stored in vault'
```

### Clear All Notes:

```
✅ "Clear all notes"
✅ "Delete all notes"

Pipoo: 🗑️ Cleared all 3 notes!
```

### Delete Specific Reminder:

```
✅ "Delete reminder 1"
✅ "Remove reminder number 2"
✅ "Cancel reminder 3"

Pipoo: 🗑️ Deleted reminder: 'call mom'
```

### Clear All Reminders:

```
✅ "Clear all reminders"
✅ "Delete all reminders"

Pipoo: 🗑️ Cleared all 3 reminders!
```

---

## 💾 **Where Data is Saved**

### Notes File:
**Location:** `C:\Users\YourName\pipoo_notes.json` (Windows)

**Content Example:**
```json
[
  {
    "content": "buy milk and eggs",
    "timestamp": "2024-11-17 14:30:15",
    "id": 1
  },
  {
    "content": "doctor appointment Thursday",
    "timestamp": "2024-11-17 14:31:22",
    "id": 2
  }
]
```

### Reminders File:
**Location:** `C:\Users\YourName\pipoo_reminders.json` (Windows)

**Content Example:**
```json
[
  {
    "content": "call mom",
    "when": "in 2 hours",
    "reminder_time": "04:30 PM today",
    "created": "2024-11-17 14:30:15",
    "id": 1
  }
]
```

---

## 🎯 **Usage Scenarios**

### Scenario 1: Shopping List

```
You: "Create a note buy milk"
Pipoo: ✅ Note saved!

You: "Create a note buy eggs"
Pipoo: ✅ Note saved!

You: "Create a note buy bread"
Pipoo: ✅ Note saved!

[At the store]
You: "Show my notes"
Pipoo: [Lists all 3 items]
```

### Scenario 2: Daily Tasks

```
You: "Remind me to workout in 1 hour"
Pipoo: ⏰ Reminder set!

You: "Remind me to call dentist tomorrow"
Pipoo: ⏰ Reminder set!

You: "Show my reminders"
Pipoo: [Shows both reminders]
```

### Scenario 3: Important Information

```
You: "Remember that my car license expires in December"
Pipoo: ✅ Note saved!

You: "Note WiFi password is HomeSweetHome123"
Pipoo: ✅ Note saved!

[Later]
You: "Show my notes"
Pipoo: [Shows all saved info]
```

---

## 🔄 **Complete Workflow Example**

```
You: "Create a note meeting with John on Friday"
Pipoo: ✅ Note saved! You now have 1 note(s).

You: "Set a reminder to prepare presentation in 2 days"
Pipoo: ⏰ Reminder set! You now have 1 reminder(s).

You: "Create a note bring laptop charger"
Pipoo: ✅ Note saved! You now have 2 note(s).

You: "Show my notes"
Pipoo: 📝 Your Notes (2 total):
       1. meeting with John on Friday
       2. bring laptop charger

You: "Show my reminders"
Pipoo: ⏰ Your Reminders (1 total):
       1. prepare presentation - in 2 days

You: "Delete note 2"
Pipoo: 🗑️ Deleted note: 'bring laptop charger'

You: "Show my notes"
Pipoo: 📝 Your Notes (1 total):
       1. meeting with John on Friday
```

---

## 🎨 **Tips & Tricks**

### 1. **Be Natural**
You don't need exact phrases:
- ✅ "hey pipoo make a note about buying milk"
- ✅ "can you create a note saying call mom"
- ✅ "write down that I need to finish homework"

### 2. **Detailed Notes**
Include all details in one note:
```
"Create a note meeting with Sarah on Thursday at 3 PM 
 at Starbucks downtown bring presentation slides"
```

### 3. **Use Reminders for Time-Sensitive Tasks**
```
"Remind me to take medicine at 9 AM"  ← Time-specific
"Create a note doctor prescribed aspirin" ← Reference info
```

### 4. **Review Before Deleting**
```
You: "Show my notes"
[Review the list]
You: "Delete note 3"
```

### 5. **Backup Your Data**
Your notes are in JSON files - you can:
- Open them in any text editor
- Copy them as backup
- Edit them manually if needed
- Share them with other devices

---

## 🐛 **Troubleshooting**

### Issue: "Note not saving"
**Check:**
- Say at least 3-4 words in the note
- Include "note" or "create" in your command
- Look for `pipoo_notes.json` in your home directory

### Issue: "Can't see my notes"
**Solution:**
```
# Check file location
Windows: C:\Users\YourName\pipoo_notes.json
Mac: /Users/YourName/pipoo_notes.json
Linux: /home/username/pipoo_notes.json
```

### Issue: "Reminder time not parsing"
**Use clear formats:**
- ✅ "in 2 hours" (not "2 hours")
- ✅ "at 8 PM" (not "8 PM")
- ✅ "tomorrow" (not "next day")

### Issue: "Deleted wrong note"
**Sorry!** Currently no undo feature. 
**Tip:** Always say "show my notes" before deleting!

---

## 📱 **Access Your Data**

### View JSON Files:

**Windows:**
```
notepad %USERPROFILE%\pipoo_notes.json
notepad %USERPROFILE%\pipoo_reminders.json
```

**Mac/Linux:**
```bash
cat ~/pipoo_notes.json
cat ~/pipoo_reminders.json
```

### Edit Manually:
Open the JSON file in any text editor and modify!

---

## ✅ **Quick Reference**

| Action | Command Examples |
|--------|-----------------|
| **Create Note** | "Create a note [text]" |
| **Show Notes** | "Show my notes" |
| **Delete Note** | "Delete note 2" |
| **Clear Notes** | "Clear all notes" |
| **Set Reminder** | "Remind me to [task] in [time]" |
| **Show Reminders** | "Show my reminders" |
| **Delete Reminder** | "Delete reminder 1" |
| **Clear Reminders** | "Clear all reminders" |

---

## 🎉 **Start Using Now!**

Try these commands right now:

1. `"Create a note test note"`
2. `"Show my notes"`
3. `"Remind me to drink water in 10 minutes"`
4. `"Show my reminders"`

**Your notes and reminders will be saved forever!** 💾

---

**Made with ❤️ for staying organized!**
*Pipoo - Your Personal Note-Taking Assistant* 🤖📝