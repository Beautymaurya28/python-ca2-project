import speech_recognition as sr

print("Available microphones:")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{index}: {name}")

print("\nTesting default microphone...")
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source, timeout=5)
    
try:
    text = r.recognize_google(audio)
    print(f"You said: {text}")
except Exception as e:
    print(f"Error: {e}")