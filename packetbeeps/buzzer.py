import RPi.GPIO as GPIO
import time

class Buzzer:

    def __init__(self):
        # Set up GPIO mode and pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)

        # Define the frequencies for different notes (in Hz)
        self.note_frequencies = [
            261,  # C4
            294,  # D4
            329,  # E4
            349,  # F4
            392,  # G4
            440,  # A4
            466,  # B4
            523  # C5
        ]

    def play_note(self, note_index):
        print(f"play_note got called with index {note_index}")
        if 0 <= note_index < len(self.note_frequencies):
            frequency = self.note_frequencies[note_index]
            # Play the note for 0.5 seconds
            for _ in range(frequency):
                GPIO.output(17, GPIO.HIGH)
                time.sleep(1 / (2 * frequency))  # Half of the period
                print(f"BEEP! {frequency}")
                GPIO.output(17, GPIO.LOW)
                time.sleep(1 / (2 * frequency))
            time.sleep(0.5)  # Delay between notes
        else:
            print("Note not recognized.")

    def stop(self):
        # Cleanup GPIO settings after usage
        GPIO.cleanup()

    def __del__(self):
        # Ensure GPIO cleanup happens when the object is destroyed
        GPIO.cleanup()
