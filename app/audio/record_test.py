import sounddevice as sd
import soundfile as sf

# Stereo mix discovered during phase 1B
DEVICE_ID = 16

# Recording Configuration
SAMPLE_RATE = 48000
CHANNELS = 2
DURATION = 60

# Output file
OUTPUT_FILE = "system_audio_test.wav"

print("Starting system audio recording...")
print(f"Device: {DEVICE_ID}")
print(f"Duration: {DURATION} seconds")
print()

audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate = SAMPLE_RATE, channels = CHANNELS, dtype = "float32", device = DEVICE_ID)

sd.wait()

sf.write(OUTPUT_FILE, audio, SAMPLE_RATE)

print("Recording Complete")
print(f"Saved to: {OUTPUT_FILE}")