"""
pip install kokoro-onnx soundfile

wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
python examples/podcast.py
"""

import soundfile as sf
from kokoro_onnx import Kokoro
import numpy as np
import random
import json

# Initialize Kokoro
kokoro = Kokoro("kokoro-v1.0.onnx", "voices.json")

# Initialize sample_rate with a default value (will be updated with actual rate from kokoro)
sample_rate = 24000  # Default sample rate for Kokoro

def random_pause(min_duration=0.5, max_duration=2.0):
    """Generate random silence duration between sentences"""
    silence_duration = random.uniform(min_duration, max_duration)
    silence = np.zeros(int(silence_duration * sample_rate))
    return silence

def load_script(json_path):
    """Load the podcast script from JSON file"""
    try:
        with open(json_path, 'r') as f:
            # Remove the ```json and ``` markers if present
            content = f.read()
            content = content.replace('```json\n', '').replace('\n```', '')
            return json.loads(content)
    except Exception as e:
        print(f"Error loading script: {str(e)}")
        return None

# Load the script from JSON
print("Loading podcast script...")
sentences = load_script("podcast_script.json")

if not sentences:
    print("Failed to load podcast script!")
    exit(1)

print(f"Loaded {len(sentences)} sentences from script")

# Generate audio
audio = []

for sentence in sentences:
    voice = sentence["voice"]
    text = sentence["text"]
    print(f"Creating audio with {voice}: {text}")
    
    try:
        samples, sample_rate = kokoro.create(
            text,
            voice=voice,
            speed=1.0,
            lang="en-us",
        )
        audio.append(samples)
        # Add random silence after each sentence
        audio.append(random_pause())
    except Exception as e:
        print(f"Error generating audio for text: {text}")
        print(f"Error: {str(e)}")
        continue

if not audio:
    print("No audio was generated!")
    exit(1)

# Concatenate all audio parts
print("Concatenating audio segments...")
audio = np.concatenate(audio)

# Save the generated audio to file
print("Saving audio to podcast.wav...")
try:
    sf.write("podcast.wav", audio, sample_rate)
    print("Successfully created podcast.wav")
except Exception as e:
    print(f"Error saving audio file: {str(e)}")