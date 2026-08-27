import whisper

MODEL_NAME = "base"
AUDIO_FILE = "system_audio_test.wav"

print("Loading Whisper model...")
model = whisper.load_model(MODEL_NAME)

print("Whisper model loaded successfully.")
print()

print("Transcribing audio... ")
result = model.transcribe(AUDIO_FILE)

print()
print("Transcription: ")
print("=" * 60)
print(result["text"])
print("=" * 60)