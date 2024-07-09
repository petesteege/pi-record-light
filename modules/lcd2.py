import threading
import time
import queue
from RPLCD.i2c import CharLCD
import shared
# Global variables for header and message
header_text = ""
message_text = ""
message_display_duration = 2.0

# Queue for thread-safe communication
lcd_queue = queue.Queue()

i2c_addr = 0x27

lcd = CharLCD('PCF8574', i2c_addr, cols=20, rows=2, charmap='A00', auto_linebreaks=True)

# Function to update header text
def sHeader(text):
    global header_text
    header_text = text
    lcd_queue.put(('update', 1))  # Indicate update and specify line 1 for header




# Function to update message text and start/reset timer
def sMessage(text):
    global message_text
    if shared.menu_displayed == True:
        message_text = "- " + text
        lcd_queue.put(('update', 2)) 
    elif shared.menu_displayed == False:
        message_text = "> " + text
        lcd_queue.put(('update', 2)) 
        if text != "RECORDING": 
            lcd_queue.put(('start_timer', time.time()))
            
            
def clear():
     lcd.clear           


# Function to clear message and display ">"
def clear_message():
    global message_text
    message_text = ""
    lcd_queue.put(('update', 2))  # Indicate update and specify line 2 for message

# Function to update LCD display
def update_lcd(line):
    if line == 1:
        lcd.cursor_pos = (0, 0)
        lcd.write_string(header_text.ljust(20))
    elif line == 2:
        lcd.cursor_pos = (1, 0)
        lcd.write_string(message_text.ljust(20) if message_text else ">                  ".ljust(20))

# LCD handler thread
def lcd_handler():
    message_start_time = None
    while True:
        if not lcd_queue.empty():  # Check if the queue is not empty
            try:
                task, line = lcd_queue.get(timeout=1)  # Wait for up to 1 second for a task
                if task == 'update':
                    update_lcd(line)
                elif task == 'start_timer':
                    message_start_time = line  # 'line' here will be the timestamp
                lcd_queue.task_done()
            except queue.Empty:
                pass  # Continue waiting if the queue is empty

        # Check if the message display duration has elapsed
        if message_start_time and (time.time() - message_start_time) > message_display_duration:
            clear_message()
            message_start_time = None

# Start the LCD handler thread
lcd_thread = threading.Thread(target=lcd_handler, daemon=True)
lcd_thread.start()

# Example usage
if __name__ == "__main__":
    try:
        sHeader("Header Text")

        # Simulating periodic message updates
        sMessage("Hello World!")
        time.sleep(1)
        sMessage("I2C LCD Display")
        time.sleep(6)
        sMessage("New Message!")
        time.sleep(0.5)

        # Keep the main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        lcd.clear()
