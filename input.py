"""
Configures a RPI 3B to use a GPIO controlled 4x4 matrix keypad and a USB barcode scanner.

The 4x4 matrix keypad is controlled with 8 GPIO pins.
Starting from the left on the keypad's cables, the first 4 cables are rows, while the last 4 cables are columns.

The USB barcode scanner (Busicom BC-BR900L-B) requires the evdev library.
This is due to the linux kernel evdev module only detecting the scanner as a generic input device.
"""
import RPi.GPIO as GPIO
from time import sleep
import evdev
import display
# pin setup for the keypad's rows and columns
rows = [4, 17, 27, 5]
columns = [6, 26, 20, 16]

def gpio_setup(rows: list, columns: list):
	"""Configures row and column pins on GPIO.

	Rows are setup as output and high.
	Columns are setup as input pins utilizing the internal pull-up resistor.
	The broadcom mode is utilized; this code assumes the physical setup uses the pi wedge.

	Args:
		rows: list of integers respresenting the GPIO pins used.
		columns: list of integers respresenting the GPIO pins used.
	"""
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	for row in rows:
		GPIO.setup(row, GPIO.OUT)
		GPIO.output(row, GPIO.HIGH)

	for column in columns:
		GPIO.setup(column, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def keypad_scan(rows: list, columns: list):
	"""Detects for a key press and returns pressed key.

	In order to detect a key press, one row at a time must be scanned (set to low).
	If a key is pressed, the respective column pin will turn to low.
	If both the row and column pin are low, then the key is detected as pressed.
	Before moving on to the next row, the current row is set back to high, repeating the process.

	Args:
		rows: list of integers respresenting the GPIO pins used.
		columns: list of integers respresenting the GPIO pins used.

	Returns:
		integer or string representing the pressed key.
	"""
	# physical keypad layout
	keys = [
		[1, 2, 3, 'A'],
		[4, 5, 6, 'B'],
		[7, 8, 9, 'C'],
		['*', 0, '#', 'D']
	]

	# "scanning"
	for row_index, row_pin in enumerate(rows):
		GPIO.output(row_pin, GPIO.LOW)

		for column_index, column_pin in enumerate(columns):
			# key is pressed
			if GPIO.input(column_pin) == GPIO.LOW:
				return keys[row_index][column_index]

		# turn that row back on
		GPIO.output(row_pin, GPIO.HIGH)

	# don't do anything if nothing is pressed
	return None


# TODO : detect if keypad is disconnected
# TODO : display active typing to LCD
def keypad_input():
	"""

	Returns:
		isbn: 10 or 13 character string representing an ISBN
	"""
	isbn = []
	while True:
		key = keypad_scan(rows, columns)

		if type(key) is int:
			isbn.append(str(key))
			print(f'isbn : {isbn}')

		# 'D' is the delete key
		elif key == 'D':
			isbn.pop(-1)
			print(f'isbn : {isbn}')

		# hashtag is the submit key
		elif key == '#':
			for number in isbn:
				isbn = ''.join(isbn)
			print(f'isbn : {isbn}')
			return isbn

		# '*' is the stop key
		elif key == '*':
			return None

		sleep(.3)

		# only limit to 13 characters for isbn13
		if len(isbn) > 13:
			isbn.pop(-1)


#TODO obtain scanner input path

def barcode_scan(path: str):
	dev = InputDevice('/dev/input/event0')
	barcode = ''
	for event in dev.read_loop():
		if event.type == ecodes.EV_KEY:
			key_event = categorize(event)
			if key_event.keystate == key_event.key_up:
				if key_event.keycode == 'KEY_ENTER':
					print("Scanned barcode:", barcode)
					barcode = ''
				else:
					barcode += key_event.keycode[4:]


# test
gpio_setup(rows, columns)
keypad_input()