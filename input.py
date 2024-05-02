"""
Configures a RPI 3B to use a GPIO controlled 4x4 matrix keypad and a USB barcode scanner.

The 4x4 matrix keypad is controlled with 8 GPIO pins.
Starting from the left on the keypad's cables, the first 4 cables are rows, while the last 4 cables are columns.

The USB barcode scanner (Busicom BC-BR900L-B) requires the evdev library.
This is due to the linux kernel evdev module only detecting the scanner as a generic input device.
"""
import RPi.GPIO as GPIO
from time import sleep
from display import *
import evdev


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
def keypad_input(rows: list, columns: list):
	"""responds to keypad presses depending on key, and displays active status to LCD.
	If pressed key is an integer, add to the list isbn.
	If pressed key is 'D', "delete" the last integer from the list isbn.
	If pressed key is '#', filter to ensure 10/13 characters then return the ISBN.
	If pressed key is '*', stop immediately.

	Returns:
		formatted_isbn: 10 or 13 character string representing an ISBN
	"""
	isbn = []
	while True:
		key = keypad_scan(rows, columns)

		if type(key) is int:
			isbn.append(str(key))
			formatted_isbn = ''.join(isbn)
			lcd_string(f'{formatted_isbn}', LCD_LINE_2)

		# 'B' is the "done inputting ISBNs key"
		elif key == 'B':
			return False

		# 'D' is the delete key
		elif key == 'D':
			isbn.pop(-1)
			formatted_isbn = ''.join(isbn)
			lcd_string(f'{formatted_isbn}', LCD_LINE_2)

		# '#' is the submit key
		elif key == '#':
			if len(isbn) >= 10:
				for number in isbn:
					formatted_isbn = ''.join(isbn)
				lcd_string(f'submitted ISBN:', LCD_LINE_1)
				lcd_string(f'{formatted_isbn}', LCD_LINE_2)
				time.sleep(3)
				return formatted_isbn
			elif len(isbn) < 10:
				lcd_string(f'ISBNS are 10/13', LCD_LINE_1)

		# '*' is the stop key
		elif key == '*':
			lcd_string(f'use scanner now', LCD_LINE_1)
			return None

		sleep(.3)

		# only limit to 13 characters for isbn13
		if len(isbn) > 13:
			isbn.pop(-1)


def scanner_setup():
	"""setups the USB barcode scanner (Busicom BC-BR900L-B).

	The linux kernel does not support this barcode scanner as a keyboard.
	As such, the evdev library must be used to take the direct input.
	This detects the barcode scanner's input path using evdev.
	With the input path, the device input can be read.

	Returns:
		barcode_scanner: str representing the barcode scanner's input path.
	"""
	devices = []

	for device in evdev.list_devices():
		evdev_device = evdev.InputDevice(device)
		devices.append(evdev_device)


	for device in devices:
		if 'Future' in device.name:
			barcode_scanner_path = device.path
			return barcode_scanner_path


def scanner_input(barcode_scanner_path: str):
	"""Reads the barcode scanner's events, filters for simulated key presses and obtains their value to form an ISBN.

	The scanner's events simulate pressing and releasing a keyboard key.
	The evdev library allows filtering through these events to only obtain keyboard events (key events).
	Since a key press has two events, push and release, this function filters only for key pushes.

	Args:
		barcode_scanner_path: str representing the barcode scanner's input path.

	Returns:
		isbn: 10 or 13 character string representing an ISBN.
	"""
	barcode_scanner = evdev.InputDevice(barcode_scanner_path)
	isbn = ''

	for event in barcode_scanner.read_loop():
		# if the event is a key event (ex: a key press)
		if event.type == evdev.ecodes.EV_KEY:
			# evdev.categorize() provides the key value and state
			key_event = evdev.categorize(event)
			# if the key_event is a key being "pressed down" and not the enter key
			# then slice string to obtain value
			if key_event.keystate == key_event.key_down and key_event.keycode != 'KEY_ENTER':
				number = key_event.keycode[4:]
				isbn += number
			elif key_event.keycode == 'KEY_ENTER':
				lcd_string(f'submitted ISBN:', LCD_LINE_1)
				lcd_string(f'{isbn}', LCD_LINE_2)
				time.sleep(3)
				return isbn


def isbns_input():
	"""Takes user input via barcode scanner and keypad scanner and returns ISBNs.

	Status of isbn input is displayed to user on LCD.
	Notifies via LCD if the scanner is unplugged.

	Returns:
		list of strings representing ISBNs.
	"""
	gpio_setup(rows, columns)
	inputting = True

	isbns = []
	while inputting is True:
		# LCD prompts user to enter ISBN
		# TODO : move into input.py functions?
		lcd_init()
		lcd_string('Enter ISBN', LCD_LINE_1)

		# do not continue if barcode scanner is not plugged in
		barcode_scanner_path = scanner_setup()
		while barcode_scanner_path is None:
			barcode_scanner_path = scanner_setup()
			lcd_string(f'scanner unpluggd', LCD_LINE_1)

		# init LCD after barcode scanner is plugged in
		lcd_init()
		lcd_string('Enter ISBN', LCD_LINE_1)

		# user enters input via keypad
		keypad_output = keypad_input(rows, columns)
		if isinstance(keypad_output, str):
			isbns.append(keypad_output)

		# press '*' on keypad to use scanner
		elif keypad_output is None:
			scanner_output = scanner_input(barcode_scanner_path)
			isbns.append(scanner_output)

		# press 'B' to stop inputting ISBNs
		elif keypad_output is False:
			lcd_string(f'requesting DLs', LCD_LINE_1)
			lcd_string(f'for ISBNs', LCD_LINE_2)
			inputting = False

	return isbns