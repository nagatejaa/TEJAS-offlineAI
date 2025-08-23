# import sounddevice as sd
# import numpy as np
# import whisper
# import torch
# import noisereduce as nr
# import re

# # ─────────── SETTINGS ───────────
# SAMPLE_RATE = 16000
# MODEL_SIZE = "small"   # tiny / base / small / medium / large
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# print(f"Loading Whisper ({MODEL_SIZE}) on {DEVICE}...")
# model = whisper.load_model(MODEL_SIZE).to(DEVICE)

# # Custom prompt bias for Whisper
# CUSTOM_PROMPT = "This audio may contain the word Tejas, which is a name."

# # ─────────── TEJAS FIX ───────────
# def fix_tejas(text: str) -> str:
#     """Replace common mis-hearings with 'Tejas'."""
#     mistakes = ["pages", "teachers", "tages", "tej us", "tajus", "tejus"]
#     for wrong in mistakes:
#         text = re.sub(rf"\b{wrong}\b", "Tejas", text, flags=re.IGNORECASE)
#     return text

# # ─────────── SIMPLE VAD ───────────
# def energy_vad(audio, threshold=0.03):
#     """Return True if audio chunk is above energy threshold (speech)."""
#     return np.sqrt(np.mean(audio**2)) > threshold

# def listen():
#     print("🎤 Speak... (Ctrl+C to stop)")
#     sentence = []
#     silence_frames = 0

#     def callback(indata, frames, time, status):
#         nonlocal sentence, silence_frames
#         audio = indata[:, 0]

#         if energy_vad(audio):  # speech detected
#             sentence.append(audio.copy())
#             silence_frames = 0
#         else:
#             silence_frames += 1

#             # If silence > ~1 sec and we have a sentence → process it
#             if silence_frames > 15 and len(sentence) > 0:
#                 audio_np = np.concatenate(sentence).astype(np.float32)

#                 # Ignore very short utterances (<0.6 sec)
#                 if len(audio_np) < SAMPLE_RATE * 0.1:
#                     sentence = []
#                     silence_frames = 0
#                     return

#                 # Noise reduction
#                 audio_np = nr.reduce_noise(y=audio_np, sr=SAMPLE_RATE)

#                 # Run Whisper with bias
#                 result = model.transcribe(
#                     audio_np,
#                     fp16=False,
#                     language="en",
#                     initial_prompt=CUSTOM_PROMPT
#                 )
#                 text = result["text"].strip()

#                 # Fix Tejas recognition
#                 text = fix_tejas(text)

#                 if text:
#                     print(f"\n🗣 You said: {text}")
#                     print("👉 Say another sentence...")

#                 # Reset buffer
#                 sentence = []
#                 silence_frames = 0

#     # Open microphone stream
#     with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, blocksize=1600, callback=callback):
#         while True:
#             sd.sleep(1000)

# if __name__ == "__main__":
#     try:
#         listen()
#     except KeyboardInterrupt:
#         print("\nStopped by user.")






import sounddevice as sd
import numpy as np
import whisper
import torch
import noisereduce as nr
import re

# ─────────── SETTINGS ───────────
SAMPLE_RATE = 16000
MODEL_SIZE = "small"   # tiny / base / small / medium / large
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading Whisper ({MODEL_SIZE}) on {DEVICE}...")
model = whisper.load_model(MODEL_SIZE).to(DEVICE)

# Context bias for Whisper
BIAS_PROMPT = "This audio may contain the word Tejas, which is a name."

# ─────────── TEXT POST-PROCESSING ───────────
def normalize_transcription(text: str) -> str:
    """Correct common misrecognitions of 'Tejas'."""
    replacements = ["pages", "teachers", "tages", "tej us", "tajus", "tejus"]
    for wrong in replacements:
        text = re.sub(rf"\b{wrong}\b", "Tejas", text, flags=re.IGNORECASE)

    # 🚫 Remove trailing period(s) if present
    text = re.sub(r"\.+$", "", text).strip()

    return text

# ─────────── VAD (VOICE ACTIVITY DETECTION) ───────────
def is_speech(audio: np.ndarray, threshold: float = 0.03) -> bool:
    """Return True if chunk energy is above threshold (likely speech)."""
    return np.sqrt(np.mean(audio**2)) > threshold

# ─────────── MAIN LISTENER ───────────
def listen():
    """Listen once, transcribe with Whisper, and return the recognized text."""
    sentence = []
    silence_frames = 0
    result_text = None  # store final text here

    def callback(indata, frames, time, status):
        nonlocal sentence, silence_frames, result_text
        if result_text is not None:  # already got result → skip
            return

        audio = indata[:, 0]

        if is_speech(audio):  # speech detected
            sentence.append(audio.copy())
            silence_frames = 0
        else:
            silence_frames += 1

            # If silence > ~1 sec and we have speech collected → process it
            if silence_frames > 15 and len(sentence) > 0:
                audio_np = np.concatenate(sentence).astype(np.float32)

                if len(audio_np) < SAMPLE_RATE * 0.1:  # Ignore too short speech
                    sentence.clear()
                    silence_frames = 0
                    return

                # Noise reduction
                audio_np = nr.reduce_noise(y=audio_np, sr=SAMPLE_RATE)
                
                # Transcribe with Whisper
                result = model.transcribe(
                    audio_np,
                    fp16=False,
                    language="en",
                    initial_prompt=BIAS_PROMPT
                )
                text = result["text"].strip()

                if text == BIAS_PROMPT.strip():
                    sentence.clear()
                    silence_frames = 0
                    return

                # Normalize "Tejas" + remove trailing periods
                result_text = normalize_transcription(text)

                print(f"You said: {result_text}")

                # Reset buffer
                sentence.clear()
                silence_frames = 0

    # Open input stream and wait until result_text is ready
    with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, blocksize=1600, callback=callback):
        print("Listening...")
        while result_text is None:
            sd.sleep(100)

    return result_text
