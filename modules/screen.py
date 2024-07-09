
import modules.lcd2 as lcd

def main():
    lcd.sHeader ("  STUDIO SERVER")
    lcd.sMessage(" ")

def wait():
    lcd.sHeader ("  STUDIO SERVER")
    lcd.sMessage("please wait ...")
    
def restart_app_wait():
    lcd.sHeader ("  Restarting APP")
    lcd.sMessage("please wait ...")
    
def reboot_sys_wait():
    lcd.sHeader ("  Rebooting SYS")
    lcd.sMessage("please wait ...")
    
def shutdown_bye():
    lcd.sHeader ("  Shutting down")
    lcd.sMessage("Good bye")