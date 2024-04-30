# BARCODE SCANNER
# from evdev import InputDevice, list_devices, categorize, ecodes
# dev = InputDevice('/dev/input/event0')
# barcode = ''
# for event in dev.read_loop():
#     if event.type == ecodes.EV_KEY:
#         key_event = categorize(event)
#         if key_event.keystate == key_event.key_up:
#             if key_event.keycode == 'KEY_ENTER':
#                 print("Scanned barcode:", barcode)
#                 barcode = ''
#             else:
#                 barcode += key_event.keycode[4:]




# PIN PAD
import RPi.GPIO as GPIO
from time import sleep
# Define the GPIO pins for the rows and columns of the keypad
rows = [4, 17, 27, 5]  # Pins for the rows
columns = [6, 26, 20, 16]  # Pins for the columns

# Define the keys on the keypad
keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]
#
# Setup GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Setup rows as outputs and initialize them to high
for row in rows:
    GPIO.setup(row, GPIO.OUT)
    GPIO.output(row, GPIO.HIGH)

# Setup columns as inputs with internal pull-up resistors
for column in columns:
    GPIO.setup(column, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to scan the keypad and return the pressed key
def scan_keypad():
    for row_index, row_pin in enumerate(rows):
        # Set the current row pin to output low
        GPIO.output(row_pin, GPIO.LOW)
        for column_index, column_pin in enumerate(columns):
            if GPIO.input(column_pin) == GPIO.LOW:
                return keys[row_index][column_index]
        # Reset the current row pin to input high
        GPIO.output(row_pin, GPIO.HIGH)
    return None

# Main loop to continuously scan the keypad
try:
    while True:
        key = scan_keypad()
        if key:
            print("Key pressed:", key)
        sleep(0.3)
except KeyboardInterrupt:
    # Clean up GPIO on Ctrl+C
    GPIO.cleanup()

