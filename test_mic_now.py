import speech_recognition as sr
import time

print("="*60)
print("MICROPHONE TEST")
print("="*60)

r = sr.Recognizer()
mic = sr.Microphone()

# Calibrate
print("\n1. Calibrating... (be quiet)")
with mic as source:
    r.adjust_for_ambient_noise(source, duration=2)
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True

print(f"   Energy threshold: {r.energy_threshold}")
print("   ✓ Calibration complete")

# Test listening
print("\n2. Listening test - SAY SOMETHING NOW!")
print("   (You have 10 seconds)")

try:
    with mic as source:
        audio = r.listen(source, timeout=10, phrase_time_limit=10)
    
    print("\n3. Processing...")
    text = r.recognize_google(audio)
    
    print(f"\n✓ SUCCESS! You said: '{text}'")
    print("\n✅ Your microphone is working!")
    
except sr.WaitTimeoutError:
    print("\n❌ TIMEOUT: No speech detected in 10 seconds")
    print("\nPossible issues:")
    print("  - Microphone is muted")
    print("  - Microphone volume too low")
    print("  - Wrong microphone selected")
    print("  - Need to speak louder")
    
except sr.UnknownValueError:
    print("\n⚠️ PARTIAL SUCCESS: Heard sound but couldn't understand")
    print("\nPossible issues:")
    print("  - Background noise too loud")
    print("  - Need to speak more clearly")
    print("  - Need to speak louder")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "="*60)