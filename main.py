"""
User enters ISBNs via barcode scanner or keypad, then the system downloads the books.
"""
from book_downloader import *
from input import *


def main():
	# STEP 1 - user enters ISBN via keypad or scanner
	isbns = isbns_input()
	# STEP 2 - begin downloading books, LCD displays active status ie progress bar
	for isbn in isbns:
		book_title, book_cover_url = isbn_info(isbn)
		download_book_cover(book_title, book_cover_url)
		download_book(book_title, isbn)
	# STEP 3 - update html to include new books
	# TODO : restart web server after
	# STEP 4 - LCD provides url when finished downloading
	# TODO : press key or wait to clear LCD


if __name__ == '__main__':
	main()