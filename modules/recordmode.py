# recordmode.py


from modules.light import *
from modules.lcd2 import sMessage

def recordmode_active():
    sMessage("RECORDING")
    rec_light(True)


def recordmode_stop():
    sMessage("stopped")
    rec_light(False)
    
