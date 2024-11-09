import RPi.GPIO as GPIO
import time

"""
testing script for buzzer. runs only on raspi
"""

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

# Generate a tone by toggling the GPIO pin
for _ in range(5):
    GPIO.output(17, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(17, GPIO.LOW)
    time.sleep(0.5)

GPIO.cleanup()
