import RPi.GPIO as GPIO
import time

def reset_all_gpio():
    try:
        # Initialize GPIO
        GPIO.setmode(GPIO.BCM)  # Set GPIO numbering mode to BCM
        
        # Iterate through all GPIO pins and reset them
        for pin in range(54):  # Adjust the range based on your GPIO chip configuration
            try:
                print(f"Resetting pin {pin} ...")
                GPIO.setup(pin, GPIO.IN)  # Set pin as input (default state)
                time.sleep(0.1)  # Adding a small delay to ensure proper reset
            except Exception as e:
                print(f"Error resetting pin {pin}: {e}")

        print("All GPIO pins reset to default state.")
        return True

    except Exception as e:
        print(f"Error during GPIO operation: {e}")
        return False

def main():
    print("Resetting GPIO pins ...")
    reset_all_gpio()
    GPIO.cleanup()  # Clean up GPIO resources
    print("Done resetting GPIO pins.")

# Call reset_all_gpio function to reset GPIO pins
if __name__ == "__main__":
    main()
