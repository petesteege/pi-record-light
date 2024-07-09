import logging
import threading
import time
from modules.led  import cleanup_led, led_power, start_network_flash_thread, led_error_flash, init_led
from modules.midi import midi_worker
from modules.gpio import cleanup_gpio, init_gpio
from modules.lcd2  import sHeader, sMessage
from modules import menus
import modules.screen as screen

import shared
logger = logging.getLogger('main')

def main():
    
    
    #cleanup_gpio()  # Ensure GPIO cleanup after completion
    
    init_gpio()
    time.sleep(1)
    #init_led()
    
    menus.setup_gpio()
    
    screen.main()
    

    try:
        led_power(2)
        
        # Start the network flash thread
        network_flash_thread = threading.Thread(target=start_network_flash_thread)
        network_flash_thread.start()

        # Initialize MIDI
        stop_event = threading.Event()
        shared.midi_thread = threading.Thread(target=midi_worker, )
        shared.midi_thread.start()
        #sMessage("  ... started MIDI") 
               
        menu_thread = threading.Thread(target=menus.start_menu_interface, args=(stop_event,))
        menu_thread.start()
        
        # Wait for threads to complete
        led_power(1)
        #sMessage("  ... done")
        
        network_flash_thread.join()
        #lcd_thread_instance.join()
        shared.midi_thread.join()
               

    except KeyboardInterrupt:
        logger.info('Got CTRL-C, quitting')
        led_power(1)
        led_error_flash()
        cleanup_led()
        stop_event.set()

    finally:
        cleanup_gpio()  # Ensure GPIO cleanup after completion

if __name__ == "__main__":
    main()
