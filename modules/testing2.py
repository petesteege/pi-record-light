import pigpio
import time

# Connect to pigpio daemon
pi = pigpio.pi()

# Pin configuration
BUTTON_PIN1 = 27
BUTTON_PIN2 = 17
BOUNCE_TIME = 300  # Debounce time in milliseconds

# Set up the button pins as inputs
pi.set_mode(BUTTON_PIN1, pigpio.INPUT)
pi.set_pull_up_down(BUTTON_PIN1, pigpio.PUD_UP)

pi.set_mode(BUTTON_PIN2, pigpio.INPUT)
pi.set_pull_up_down(BUTTON_PIN2, pigpio.PUD_UP)

# Initialize the last pressed time for both buttons
last_pressed1 = 0
last_pressed2 = 0

def button_callback1(gpio, level, tick):
    global last_pressed1
    current_time = time.time() * 1000  # Convert to milliseconds
    if (current_time - last_pressed1) > BOUNCE_TIME:
        print("Button 1 was pressed!")
        last_pressed1 = current_time

def button_callback2(gpio, level, tick):
    global last_pressed2
    current_time = time.time() * 1000  # Convert to milliseconds
    if (current_time - last_pressed2) > BOUNCE_TIME:
        print("Button 2 was pressed!")
        last_pressed2 = current_time

# Set up the callbacks for the button pins
cb1 = pi.callback(BUTTON_PIN1, pigpio.FALLING_EDGE, button_callback1)
cb2 = pi.callback(BUTTON_PIN2, pigpio.FALLING_EDGE, button_callback2)

try:
    # Keep the program running to wait for button press events
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated")

# Clean up the callbacks and disconnect from pigpio daemon
cb1.cancel()
cb2.cancel()
pi.stop()
