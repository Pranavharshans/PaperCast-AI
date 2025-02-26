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

# fmt: off
sentences = [
]

def random_pause(min_duration=0.5, max_duration=2.0):
    silence_duration = random.uniform(min_duration, max_duration)
    silence = np.zeros(int(silence_duration * sample_rate))
    return silence


kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")

audio = []

for sentence in sentences:
    voice = sentence["voice"]
    text = sentence["text"]
    print(f"Creating audio with {voice}: {text}")
    
    samples, sample_rate = kokoro.create(
        text,
        voice=voice,
        speed=1.0,
        lang="en-us",
    )
    audio.append(samples)
    # Add random silence after each sentence
    audio.append(random_pause())

# Concatenate all audio parts
audio = np.concatenate(audio)

# Save the generated audio to file
sf.write("podcast.wav", audio, sample_rate)
print("Created podcast.wav")