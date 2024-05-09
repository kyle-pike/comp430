"""
User enters ISBNs via barcode scanner or keypad, then the system downloads the books.

Downloads books to relative path 'books/'.
Downloads book covers to relative path 'imgs/'.
"""
from book_downloader import *
from input import *
from update_html import *
from display import *


def main():
	while True:
		# STEP 1 - user enters ISBN(s) via keypad or scanner
		isbns = isbns_input()

		# STEP 2 - download book(s)
		for isbn in isbns:
			book_title, book_cover_url = isbn_info(isbn)

			# if the ISBN is real
			if isinstance(book_title, str):
				book_cover_img = download_book_cover(book_title, book_cover_url)
				book_file = download_book(book_title, isbn)

			# if the ISBN doesn't exist
			elif isinstance(book_title, bool):
				lcd_string(f'ISBN null', LCD_LINE_1)
				lcd_string(f'{isbn}', LCD_LINE_2)
				time.sleep(3)
				continue  # skip all code below in this loop and move to next ISBN

			# unable to connect to openlibrary.org
			else:
				lcd_string(f"Can't connect", LCD_LINE_1)
				lcd_string(f'to openlibrary', LCD_LINE_2)
				time.sleep(3)
				continue  # skip all code below in this loop and move to next ISBN

		# STEP 3 - update html to include new books
			if book_cover_img and book_file is not None:
				html_file = 'index.html'
				update_html(html_file, book_cover_img, book_title, book_file)
				lcd_string('downloaded', LCD_LINE_1)
				lcd_string(f'{isbn}', LCD_LINE_2)
				time.sleep(3)
			else:  # don't update html file if book was not downloaded
				lcd_string(f'unable to fetch', LCD_LINE_1)
				lcd_string(f'{isbn}', LCD_LINE_2)
				time.sleep(3)


if __name__ == '__main__':
	main()