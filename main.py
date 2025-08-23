from FUNCTION.wish import wish
from FUNCTION.welcome import welcome
from HEAD.ear import listen
from HEAD.brain import mind
from HEAD.mouth import speak
import time

def tejas():
    speak("TEJAS activated")
    speak("Waiting for wake word")
    
    # ─── Phase 1: Wait for wake word ───
    while True:
        text = listen()
        print(f"Wake word check: {text}")
        if "tejas" in text.lower():
            time.sleep(3)
            welcome()
            break   # wake word detected → exit loop
        else:
            speak("Waiting for wake word")
    
    # ─── Phase 2: Assistant active ───

    speak("I'm listening...")
    while True:
        text = listen()
        
        if text in ["exit", "quit", "stop"]:
            speak("Shutting down. Goodbye!")
            break
        else:
            mind(text)  # your main brain function

tejas()
