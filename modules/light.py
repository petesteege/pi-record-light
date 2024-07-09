# light.py

import RPi.GPIO as GPIO

# Set up the GPIO pin number
RECORD_LIGHT_PIN = 18 

# Initialize the GPIO settings

def rec_light(is_recording):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECORD_LIGHT_PIN, GPIO.OUT)
    
    if is_recording:
        GPIO.output(RECORD_LIGHT_PIN, GPIO.HIGH)  # Turn on the light
        print("Record light is ON")
    else:
        GPIO.output(RECORD_LIGHT_PIN, GPIO.LOW)   # Turn off the light
        print("Record light is OFF")

def cleanup_light():
    GPIO.cleanup()
