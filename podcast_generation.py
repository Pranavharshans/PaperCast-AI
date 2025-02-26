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

# Direct sentences array
sentences = [
  {
    "voice": "af_sarah",
    "text": "Hey everyone, welcome back to the show! Today we're talking about something super important, but maybe a little dry: infrastructure. Specifically, how AI can help keep our bridges from crumbling. Michael, ready to make this exciting?"
  },
  {
    "voice": "am_michael",
    "text": "Absolutely, Sarah! Bridges might seem boring until you're stuck in traffic because one's closed for repairs. So, let's talk about how AI is stepping in to save the day... and maybe our commutes!"
  },
  {
    "voice": "af_sarah",
    "text": "Exactly! This research paper we're diving into is titled 'Benchmarking YOLOv8 for Optimal Crack Detection in Civil Infrastructure.' Basically, it's about using a fancy AI model to find cracks in bridges before they become big problems."
  },
  {
    "voice": "am_michael",
    "text": "Okay, 'YOLOv8' sounds like something out of a sci-fi movie. What exactly is it?"
  },
  {
    "voice": "af_sarah",
    "text": "Think of YOLOv8 as a super-smart detective for images. It's a type of AI model designed for object detection – in this case, detecting cracks. The 'YOLO' part stands for 'You Only Look Once,' meaning it can analyze an image really quickly."
  },
  {
    "voice": "am_michael",
    "text": "So, instead of a human inspector with binoculars, we have an AI that can scan bridge images and pinpoint cracks in real-time? That's pretty cool."
  },
  {
    "voice": "af_sarah",
    "text": "Exactly! And the paper explores different versions of YOLOv8, like 'nano,' 'small,' 'medium,' 'large,' and 'extra-large.' Each one is a slightly different size and optimized for different trade-offs between speed and accuracy."
  },
  {
    "voice": "am_michael",
    "text": "Like choosing between a scooter and a truck, depending on what you need to carry, right?"
  },
  {
    "voice": "af_sarah",
    "text": "Perfect analogy! The researchers also tested different 'optimizers,' which are like different training methods that help the AI learn to detect cracks more effectively. They found that using something called 'Stochastic Gradient Descent,' or SGD, worked really well with the 'medium' version of YOLOv8."
  },
  {
    "voice": "am_michael",
    "text": "Stochastic Gradient Descent... that sounds intimidating. Can you break that down?"
  },
  {
    "voice": "af_sarah",
    "text": "Imagine you're trying to find the lowest point in a valley, but you're blindfolded. SGD is like taking small, random steps downhill until you reach the bottom. It's a way to fine-tune the AI's crack-detecting abilities."
  },
  {
    "voice": "am_michael",
    "text": "Okay, that makes sense! So, what were the big takeaways from this research?"
  },
  {
    "voice": "af_sarah",
    "text": "The main finding is that YOLOv8, especially the medium version with the SGD optimizer, is a really promising tool for detecting cracks in bridges quickly and accurately. This could lead to more proactive maintenance, preventing bigger problems and saving money in the long run."
  },
  {
    "voice": "am_michael",
    "text": "So, fewer traffic jams and safer bridges? Sounds like a win-win! But what's next for this research?"
  },
  {
    "voice": "af_sarah",
    "text": "The researchers acknowledge that they used a limited dataset of crack images. They plan to expand this dataset to include more diverse types of cracks and environmental conditions. This will make the AI even more robust and reliable in real-world scenarios."
  },
  {
    "voice": "am_michael",
    "text": "That makes sense. The more the AI 'sees,' the better it gets at spotting those sneaky cracks."
  },
  {
    "voice": "af_sarah",
    "text": "Exactly! And this isn't just about bridges. This technology could be applied to other infrastructure, like buildings and highways, making our world a safer place."
  },
  {
    "voice": "am_michael",
    "text": "It's amazing how AI is being used to solve real-world problems. Who knew crack detection could be so fascinating?"
  },
  {
    "voice": "af_sarah",
    "text": "Right? So, to wrap up, AI, specifically YOLOv8, can revolutionize infrastructure maintenance by quickly and accurately detecting cracks. This leads to safer structures, fewer repairs, and ultimately, a more reliable transportation system."
  },
  {
    "voice": "am_michael",
    "text": "Definitely something to appreciate the next time you're cruising over a bridge! Thanks for breaking down this research, Sarah."
  },
  {
    "voice": "af_sarah",
    "text": "My pleasure, Michael! And thanks to our listeners for tuning in. If you're interested in learning more about AI and infrastructure, check out the research paper linked in the show notes. Until next time, stay curious!"
  }
]

kokoro = Kokoro("kokoro-v1.0.onnx", "voices.json")

# Initialize sample_rate with a default value (will be updated with actual rate from kokoro)
sample_rate = 24000  # Default sample rate for Kokoro

def random_pause(min_duration=0.5, max_duration=2.0):
    silence_duration = random.uniform(min_duration, max_duration)
    silence = np.zeros(int(silence_duration * sample_rate))
    return silence

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