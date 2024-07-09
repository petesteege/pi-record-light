import mido
import logging
import threading
import shared
from modules.recordmode import recordmode_active, recordmode_stop
from modules.led import led_error_flash, led_midi_data_flash

logger = logging.getLogger('midi')

recording = False
recording_lock = threading.Lock()

def midi_worker():
    try:
        # Find all available MIDI input ports
        ports = mido.get_input_names()
        print("Available MIDI Ports:", ports)

        if not ports:
            led_error_flash()
            logger.error("No MIDI input ports available.")
            return

        # Open all MIDI input ports
        midi_inputs = []
        for port_name in ports:
            try:
                midi_in = mido.open_input(port_name)
                midi_in.callback = lambda msg: message_handler(msg, shared.midi_stop_event)  # Pass stop_event to message_handler
                midi_inputs.append(midi_in)
                logger.info("Opened MIDI input port: %s", port_name)
            except Exception as e:
                logger.error("Failed to open MIDI input port %s: %s", port_name, str(e))

        if not midi_inputs:
            logger.error("Failed to open any MIDI input ports.")
            return

        # Keep the main thread alive until stop event is set
        while not shared.midi_stop_event.is_set():
            pass  # Your MIDI processing logic here

        # Close MIDI input ports
        for midi_in in midi_inputs:
            midi_in.close()

    except Exception as e:
        logger.exception("Error initializing MIDI: %s", e)

    logger.info("MIDI worker thread stopped.")


def message_handler(message, stop_event):
    global recording

    try:
        print("[MIDI] Received MIDI message:", message)
        led_midi_data_flash()

        if message.type == 'note_on':
            note_name = message.note
            velocity = message.velocity
            logger.info('MIDI Note On: Note Name: {}, Velocity: {}'.format(note_name, velocity))

            with recording_lock:
                if note_name == 25 and velocity == 127:
                    if not recording:
                        recording = True
                        recordmode_active()
                else:
                    if recording:
                        recording = False
                        recordmode_stop()
        else:
            logger.info('MIDI Command: {}'.format(message))

    except Exception as e:
        logger.exception("Error handling MIDI message: %s", e)
