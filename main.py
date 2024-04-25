from book_downloader import *
from display import *
from input import *

def main():

	'''
	----- PROCESS -----
	1) LCD : enter ISBN
	2) * user enters isbn via pin pad or scanner *
		function that deletes or backspace if messed up ISBN via pin pad
	3) LCD : $ISBN, request another?
	4) * user inputs more ISBNs or presses key on pin pad to finish *
	5) LCD : grabs status from book_downloader.py, ex: downloading $book_title
	6) LCD : finished, please obtain books via $URL
	7) LCD : return to start?
	restarts process
	'''

	isbn = '9780813054964'
	book_title = isbn_info(isbn)
	print(f'attempting to download : {book_title}')

	anna_html = download_anna_html(isbn)
	hashes = parse_anna_html(anna_html)
	provider, valid_hash, file_type = parse_anna_hashes(hashes)

	if provider == 'libgen':
		libgen_html = download_libgen_html(valid_hash)
		key = parse_libgen_html(libgen_html)
		download_libgen_book(book_title, file_type, valid_hash, key)

	elif provider == 'libraryLOL':
		libraryLOL_html = download_libraryLOL_html(valid_hash)
		download_libraryLOL_book(book_title, file_type, libraryLOL_html)

	else:
		print('no provider found')


if __name__ == '__main__':
	main()