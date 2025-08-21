
###OFFLINE VOICE
import os
import pygame
from TTS.api import TTS

# ───────────────────────────── CONFIG ─────────────────────────────
MODEL_NAME = "tts_models/en/vctk/vits"   # more natural, many speakers
OUTPUT_FILE = "output.wav"
SPEAKER = "p233"  # pick a deeper/male voice (try others like "p225", "p270")

# ───────────────────────────── TTS FUNCTION ───────────────────────
def speak(text):
    try:
        # Initialize TTS with chosen model
        tts = TTS(MODEL_NAME, progress_bar=False, gpu=False)

        # Convert text to speech
        tts.tts_to_file(text=text, speaker=SPEAKER, file_path=OUTPUT_FILE)

        # Play audio
        pygame.mixer.init()
        sound = pygame.mixer.Sound(OUTPUT_FILE)
        sound.play()

        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)

        # Clean up
        pygame.mixer.quit()
        os.remove(OUTPUT_FILE)
        print("Played and deleted:", OUTPUT_FILE)

    except Exception as e:
        print(f"Error: {e}")


