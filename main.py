"""

"""
from book_downloader import *
from display import *
from input import *


def main():

	gpio_setup()

	while True:
		# STEP 1 - LCD prompts user to enter ISBN
		lcd_init()
		lcd_string('Enter ISBN', 0)

		# STEP 2 - user enters ISBN via keypad or scanner
		keypad_output = keypad_input()
		if keypad_output is None:


		# STEP 3 - LCD displays the entered ISBN and if they want to download another
		lcd_init()
		lcd_string(f'ISBN : {isbn}', 0)
		lcd_string('Press * to stop inputting.', 1)

		# STEP 4 - user inputs more ISBNs or presses * on keypad to finish
		keypad_output = keypad_input()
		if keypad_output is None:
			print('done entering')
		# STEP 5 - begin downloading books, LCD displays active status ie progress bar
		for isbn in isbns:
			book_title, book_cover_url = isbn_info(isbn)
			download_book_cover(book_title, book_cover_url)
			download_book(book_title, isbn)
		# STEP 6 - update html to include new books
		# TODO : restart web server after
		# STEP 7 - LCD provides url when finished downloading
		# TODO : press key or wait to clear LCD





if __name__ == '__main__':
	main()