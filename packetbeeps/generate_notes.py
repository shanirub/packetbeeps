"""
script for generating wav files for music notes.

run only once on pc.

maybe i'll use wavs created in the future
"""

import numpy as np
from scipy.io.wavfile import write

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
