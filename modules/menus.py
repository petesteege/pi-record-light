import threading
import time
import pigpio
import subprocess
import modules.lcd2 as lcd2
import modules.led as led
import shared  # Adjust as per your pin configuration
from modules.led import led_power_flashonce
import modules.recordmode as recordmode

import modules.screen as screen
import modules.system as sys


# Menu Data
menus = [
    {"h": "1 MENU", "m": "scroll"},
    {"h": "2 NET / IP", "m": f"{sys.get_ip()}"},
    {"h": "3 NET / MAC", "m": f"{sys.get_mac()}"},
    {"h": "4 MIDI / RTP name", "m": f"{sys.get_rtp()}"},
    {"h": "5 SYS / shutdown", "m": "yes? (enter)"},
    {"h": "6 SYS /restart app", "m": "yes? (enter)"},
    {"h": "7 SYS / restart sys", "m": "yes? (enter)"},
    {"h": "8 TEST / record", "m": "turn ON   (enter)"},
    {"h": "9 EXIT / MENU", "m": "exit? (enter)"}
]

current_menu = 0

toggle_record_test_flag = 0

# GPIO setup using pigpio
pi = pigpio.pi()


def display_menu(index):
    lcd2.sHeader(menus[index]['h'])
    lcd2.sMessage(menus[index]['m'])

def handle_down_button(gpio, level, timestamp):
    global current_menu
    if shared.menu_displayed:
        led_power_flashonce()
        current_menu = (current_menu + 1) % len(menus)
        display_menu(current_menu)

def handle_select_button(gpio, level, timestamp):
    global current_menu
    if not shared.menu_displayed:
        led_power_flashonce()
        #stop_midi_thread()
        shared.menu_displayed = True
        display_menu(current_menu)
    else:
        # Handle select action based on current menu item
        if current_menu == 4:  # Shutdown
            mnu_shutdown()
        elif current_menu == 5:  # Restart app
            mnu_restart_app()
        elif current_menu == 6:  # Restart system
            mnu_reboot()
        elif current_menu == 7:  # Test record
            toggle_record_test()
        elif current_menu == 8:
            #exitmenu
            mnu_exit()

def stop_midi_thread():
    global midi_thread  # Assuming midi_thread is a global variable in your application

    if shared.midi_thread and shared.midi_thread.is_alive():  # Check if midi_thread exists and is running
        shared.midi_stop_event.set()  # Signal the MIDI thread to stop

def setup_gpio():
    try:
        # Setup button pins as inputs with pull-up resistors
        pi.set_mode(shared.BUTTON_DOWN_PIN, pigpio.INPUT)
        pi.set_pull_up_down(shared.BUTTON_DOWN_PIN, pigpio.PUD_UP)
        pi.set_mode(shared.BUTTON_SELECT_PIN, pigpio.INPUT)
        pi.set_pull_up_down(shared.BUTTON_SELECT_PIN, pigpio.PUD_UP)

        # Add event detection for buttons
        pi.callback(shared.BUTTON_DOWN_PIN, pigpio.FALLING_EDGE, handle_down_button)
        pi.callback(shared.BUTTON_SELECT_PIN, pigpio.FALLING_EDGE, handle_select_button)

    except Exception as e:
        print(f"Failed to setup GPIO: {e}")

def start_menu_interface(stop_event):
    try:
        while True:
            time.sleep(1)  # Replace with actual logic of your main program

    except KeyboardInterrupt:
        pass
    
################### MENU HANDLING ROUTINES ########################

def mnu_exit():
   # lcd2.clear()
    shared.menu_displayed = False
    current_menu = 0
    screen.main()
    
def mnu_reboot():
    screen.reboot_sys_wait()   
    led.cleanup_led() 
    shared.midi_stop_event.set()
    time.sleep(1.5)
    sys.reboot_sys()
    
def mnu_restart_app():
    screen.restart_app_wait()
    led.cleanup_led()
    shared.midi_stop_event.set()
    time.sleep(1.5)
    sys.restart_app()
    
def mnu_shutdown():
    screen.shutdown_bye()
    led.cleanup_led()
    shared.midi_stop_event.set()
    time.sleep(1.5)
    sys.shutdown()

    
def toggle_record_test():
    global toggle_record_test_flag
    
    if toggle_record_test_flag ==0:
        recordmode.recordmode_active()
        toggle_record_test_flag = 1
        lcd2.sMessage("turn OFF (enter)")
        return
    elif toggle_record_test_flag ==1:
        recordmode.recordmode_stop()
        toggle_record_test_flag = 0
        lcd2.sMessage("turn ON (enter)")
        return
    
    
