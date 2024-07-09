import threading

mMsg = "> "
mMsg_lock = threading.Lock()

midi_thread = ""
midi_stop_event = threading.Event()  # Define the stop event

menu_displayed = False

h = -1

# GPIO setup
BUTTON_DOWN_PIN = 17  # Replace with your actual GPIO pin number
BUTTON_SELECT_PIN = 27  # Replace with your actual GPIO pin number
RECORD_LIGHT_PIN = 14  # Example 

# Define GPIO pins for LEDs
LED_POWER_PIN = 21
LED_NETWORK_PIN = 26
LED_MIDI_PIN = 20
LED_ERROR_PIN = 16


conf_file_path = '/etc/rtpmidid/rtpmidi.conf'




def update_mMsg(new_msg):
    global mMsg
    with mMsg_lock:
        mMsg = new_msg

def get_mMsg():
    global mMsg
    with mMsg_lock:
        return mMsg