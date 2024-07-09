import pigpio
import threading
import time
from modules.menus import handle_down_button, handle_select_button
from shared import *  # Import GPIO pin assignments

# Initialize pigpio

pi = None  # Define pi globally

def init_gpio():
    global pi
    try:
        pi = pigpio.pi()
        if pi is not None:
            pi.set_mode(RECORD_LIGHT_PIN, pigpio.OUTPUT)
            pi.set_mode(BUTTON_DOWN_PIN, pigpio.INPUT)
            pi.set_pull_up_down(BUTTON_DOWN_PIN, pigpio.PUD_UP)
            pi.set_glitch_filter(BUTTON_DOWN_PIN, 10000)  # Set debounce time to 10 milliseconds (10000 microseconds)

            pi.set_mode(BUTTON_SELECT_PIN, pigpio.INPUT)
            pi.set_pull_up_down(BUTTON_SELECT_PIN, pigpio.PUD_UP)
            pi.set_mode(LED_POWER_PIN, pigpio.OUTPUT)
            pi.set_mode(LED_NETWORK_PIN, pigpio.OUTPUT)
            pi.set_mode(LED_MIDI_PIN, pigpio.OUTPUT)
            pi.set_mode(LED_ERROR_PIN, pigpio.OUTPUT)
            pi.write(LED_POWER_PIN, pigpio.LOW)
            pi.write(LED_NETWORK_PIN, pigpio.LOW)
            pi.write(LED_MIDI_PIN, pigpio.LOW)
            pi.write(LED_ERROR_PIN, pigpio.LOW)
            return True
        else:
            print("Failed to initialize pigpio.pi() object")
            return False
    except Exception as e:
        print(f"ERROR: could not initialise GPIO - {e}")
        return False


def cleanup_gpio():
    try:
        pi.stop()
    except:
        pass

# Function to poll GPIO inputs
def poll_gpio():
    while True:
        try:
            # Poll BUTTON_DOWN_PIN
            if pi.read(BUTTON_DOWN_PIN) == 0:
                handle_down_button(0)  # Assuming handle_down_button expects 0 for button press

            # Poll BUTTON_SELECT_PIN
            if pi.read(BUTTON_SELECT_PIN) == 0:
                handle_select_button(0)  # Assuming handle_select_button expects 0 for button press

            time.sleep(0.1)  # Polling interval
        except KeyboardInterrupt:
            break

# Main function to initialize and use GPIO
def main():
    try:
        if init_gpio():
            print("GPIO initialization successful")

            # Start polling thread
            poll_thread = threading.Thread(target=poll_gpio, daemon=True)
            poll_thread.start()

            # Your main program logic here
            while True:
                # Example: Perform tasks or wait
                time.sleep(1)
        else:
            print("GPIO initialization failed. Exiting.")
    except KeyboardInterrupt:
        print("\nExiting program due to KeyboardInterrupt")
    finally:
        cleanup_gpio()
        print("GPIO cleanup completed. Exiting program.")

if __name__ == "__main__":
    main()
