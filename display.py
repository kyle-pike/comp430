import RPi.GPIO as GPIO
import time, smbus

# LCD pin assignments, constants, etc
I2C_ADDR = 0x27  # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

LCD_BACKLIGHT = 0x08  # On
# LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100  # Enable it

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# LCD commands
LCD_CMD_4BIT_MODE = 0x28  # 4 bit mode, 2 lines, 5x8 font
LCD_CMD_CLEAR = 0x01
LCD_CMD_HOME = 0x02  # goes to position 0 in line 0
LCD_CMD_POSITION = 0x80  # Add this to DDRAM address

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)

# Open I2C interface
bus = smbus.SMBus(1)


def lcd_init():
	"""
	Initialise display
	"""
	lcd_byte(0x33,LCD_CMD) # 110011 Initialise
	lcd_byte(0x32,LCD_CMD) # 110010 Initialise
	lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
	lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
	lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
	lcd_byte(0x01,LCD_CMD) # 000001 Clear display
	time.sleep(E_DELAY)


def lcd_byte(bits, mode):
	"""
	Send byte to data pins
	bits = the data
	mode = 1 for data , 0 for command
	"""
	bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
	bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT
	# High bits
	bus.write_byte(I2C_ADDR, bits_high)
	lcd_toggle_enable(bits_high)
	# Low bits
	bus.write_byte(I2C_ADDR, bits_low)
	lcd_toggle_enable(bits_low)


def lcd_toggle_enable(bits):
	"""
	Toggle enable
	"""
	time.sleep(E_DELAY)
	bus.write_byte(I2C_ADDR, (bits | ENABLE))
	time.sleep(E_PULSE)
	bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
	time.sleep(E_DELAY)


def lcd_string(message,line):
	"""
	Send string to display
	"""
	message = message.ljust(LCD_WIDTH," ")
	lcd_byte(line, LCD_CMD)
	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]),LCD_CHR)


def lcd_xy(col, row):
	"""
	Positions the cursor so that the next write to the LCD
	appears at a specific row & column, 0-org'd
	"""
	lcd_byte(LCD_CMD_POSITION+col+(64*row), LCD_CMD)


def lcd_msg(msg_string):
	"""
	Begins writing a string to the LCD at the current cursor
	position. It doesn't concern itself with whether the cursor
	is visible or not. Go off the screen? Your bad.
	"""
	for i in range(0, len(msg_string)):
		lcd_byte(ord(msg_string[i]), LCD_CHR)