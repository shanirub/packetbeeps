"""
script for generating wav files for music notes.
those notes will be used in mock
"""

import numpy as np
from scipy.io.wavfile import write
import os

def generate_tone(frequency, duration, sample_rate=44100, amplitude=32767):
    """Generate a pure tone and save it as a .wav file."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = amplitude * np.sin(2 * np.pi * frequency * t)
    waveform = waveform.astype(np.int16)  # Convert to 16-bit PCM
    return waveform

notes = {
    "C4": 262,
    "D4": 294,
    "E4": 330,
    "F4": 349,
    "G4": 392,
    "A4": 440,
    "B4": 494,
    "C5": 523
}

for note, freq in notes.items():
    tone = generate_tone(freq, 0.5)  # 2-second duration
    write(f"{note}.wav", 44100, tone)
    print(f"{note}.wav created!")

"""
loading the files in code:

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(BASE_DIR, 'assets', 'sounds')

c4_file = os.path.join(SOUND_DIR, 'C4.wav')
print(f"Playing: {c4_file}")
"""