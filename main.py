"""
User enters ISBNs via barcode scanner or keypad, then the system downloads the books.

Downloads books to relative path 'web_server/books/'.
Downloads book covers to relative path 'web_server/imgs/'.
"""
from book_downloader import *
from input import *
from update_html import *


def main():
	while True:
		# STEP 1 - user enters ISBN via keypad or scanner
		isbns = isbns_input()

		# STEP 2 - begin downloading books,
		# TODO : LCD displays active status ie progress bar
		for isbn in isbns:
			book_title, book_cover_url = isbn_info(isbn)

			if book_title and book_cover_url is not None:
				book_cover_img = download_book_cover(book_title, book_cover_url)
				book_file = download_book(book_title, isbn)
			else: # if isbn doesn't exist
				lcd_string(f'ISBN null', LCD_LINE_1)
				lcd_string(f'{isbn}', LCD_LINE_2)
				book_cover_img = None
				book_file = None

		# STEP 3 - update html to include new books
			if book_cover_img and book_file is not None:
				html_file = 'index.html'
				update_html(html_file, book_cover_img, book_title, book_file)
			else:  # don't update html file if book was not downloaded
				lcd_string(f'unable to fetch', LCD_LINE_1)
				lcd_string(f'{isbn}', LCD_LINE_2)

		# STEP 4 - LCD provides url when finished downloading
		lcd_init()
		lcd_string('download books', LCD_LINE_1)
		lcd_string(f'via url', LCD_LINE_2)
		time.sleep(5)


if __name__ == '__main__':
	main()