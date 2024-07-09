import threading
from RPLCD.i2c import CharLCD

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

# Global variables for header and message
header_text = ""
message_text = ""
message_display_duration = 2.0

# Lock for thread-safe access to message variables
lock = threading.Lock()

# Timer variables
timer = None
timer_running = False

i2c_addr = 0x27

lcd = CharLCD('PCF8574', i2c_addr, cols=20, rows=2, charmap='A00', auto_linebreaks=True)


# Function to update header text
def sHeader(text):
    global header_text
    with lock:
        header_text = text
    update_lcd()

# Function to update message text and start/reset timer
def sMessage(text):
    global message_text, timer, timer_running
    with lock:
        message_text = "> " + text
    update_lcd()
    
    if timer_running:
        timer.cancel()  # Cancel previous timer if running
    
    # Start new timer for 2 seconds
    timer = threading.Timer(message_display_duration, clear_message)
    timer.start()
    timer_running = True

# Function to clear message and display ">"
def clear_message():
    global message_text, timer_running
    with lock:
        message_text = ""
    update_lcd()
    timer_running = False

# Function to update LCD display
def update_lcd():
    global header_text, message_text
    with lock:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string(header_text.ljust(20))
        lcd.cursor_pos = (1, 0)
        lcd.write_string(message_text.ljust(20) if message_text else ">                  ".ljust(20))
