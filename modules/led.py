import pigpio
import threading
import psutil
from time import sleep
import shared

# Define LED flash intervals
FLASH_INTERVAL_POWER = 0.5  # in seconds
FLASH_INTERVAL_ERROR = 0.125  # in seconds

# Threading events for controlling LED flashing
stop_event_power = threading.Event()
stop_event_network = threading.Event()

# Initialize pigpio
pi = pigpio.pi()

def init_led():
    # Setup GPIO pins for LEDs
    pi.set_mode(shared.LED_POWER_PIN, pigpio.OUTPUT)
    pi.set_mode(shared.LED_NETWORK_PIN, pigpio.OUTPUT)
    pi.set_mode(shared.LED_MIDI_PIN, pigpio.OUTPUT)
    pi.set_mode(shared.LED_ERROR_PIN, pigpio.OUTPUT)
    pi.write(shared.LED_POWER_PIN, pigpio.LOW)
    pi.write(shared.LED_NETWORK_PIN, pigpio.LOW)
    pi.write(shared.LED_MIDI_PIN, pigpio.LOW)
    pi.write(shared.LED_ERROR_PIN, pigpio.LOW)

def turn_on_led(pin):
    pi.write(pin, pigpio.HIGH)

def turn_off_led(pin):
    pi.write(pin, pigpio.LOW)

def flash_power_led():
    while not stop_event_power.is_set():
        turn_on_led(shared.LED_POWER_PIN)
        sleep(FLASH_INTERVAL_POWER)
        turn_off_led(shared.LED_POWER_PIN)
        sleep(FLASH_INTERVAL_POWER)

def led_power_flashonce():
    turn_off_led(shared.LED_POWER_PIN)
    sleep(0.2)
    turn_on_led(shared.LED_POWER_PIN)

def flash_network_led():
    while not stop_event_network.is_set():
        prev_counters = psutil.net_io_counters()
        stop_event_network.wait(0.1)  # Wait for 0.1 seconds or until the event is set
        current_counters = psutil.net_io_counters()
        if (current_counters.bytes_recv != prev_counters.bytes_recv) or (current_counters.bytes_sent != prev_counters.bytes_sent):
            turn_on_led(shared.LED_NETWORK_PIN)
            sleep(0.1)  # Flash quickly
            turn_off_led(shared.LED_NETWORK_PIN)
        else:
            turn_off_led(shared.LED_NETWORK_PIN)

def start_power_flash_thread():
    global power_flash_thread
    stop_event_power.clear()
    power_flash_thread = threading.Thread(target=flash_power_led, daemon=True)
    power_flash_thread.start()

def stop_power_flash_thread():
    stop_event_power.set()
    power_flash_thread.join()

def start_network_flash_thread():
    global network_flash_thread
    stop_event_network.clear()
    network_flash_thread = threading.Thread(target=flash_network_led, daemon=True)
    network_flash_thread.start()

def stop_network_flash_thread():
    stop_event_network.set()
    network_flash_thread.join()

def led_power(state):
    if state == 0:
        stop_power_flash_thread()
        turn_off_led(shared.LED_POWER_PIN)
    elif state == 1:
        stop_power_flash_thread()
        turn_on_led(shared.LED_POWER_PIN)
    elif state == 2:
        start_power_flash_thread()
    else:
        print("Invalid state value for led_power function")

def led_midi_data_flash():
    turn_on_led(shared.LED_MIDI_PIN)
    sleep(0.1)  # Adjust if necessary
    turn_off_led(shared.LED_MIDI_PIN)

def led_error_flash():
    turn_on_led(shared.LED_ERROR_PIN)
    sleep(FLASH_INTERVAL_ERROR)
    turn_off_led(shared.LED_ERROR_PIN)

def cleanup_led():
    # Stop the LED flash threads
    stop_power_flash_thread()
    stop_network_flash_thread()
    
    # Turn on all LEDs
    turn_on_led(shared.LED_POWER_PIN)
    turn_on_led(shared.LED_NETWORK_PIN)
    turn_on_led(shared.LED_MIDI_PIN)
    turn_on_led(shared.LED_ERROR_PIN)
    
    # Cleanup pigpio
    pi.stop()
