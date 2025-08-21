from TTS.api import TTS

# Download and load model (first time takes time)
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

# Save audio to file
tts.tts_to_file(text="Hello, this is offline speech synthesis.", file_path="output.wav")

print("Speech saved to output.wav")
