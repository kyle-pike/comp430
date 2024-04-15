from book_downloader import *


def main():

	# ISBN = input("please enter the ISBN13 : ")
	isbn = '9780767908184'
	book_title = isbn_info(isbn)
	# TODO, ask user if book title is correct, reprompt isbn if not
	print(f'attempting to download : {book_title}')

	anna_html = download_anna_html(isbn)
	hashes = parse_anna_html(anna_html)
	provider, valid_hash, file_type = parse_anna_hashes(hashes)

	if provider == 'libgen':
		libgen_html = download_libgen_html(valid_hash)
		key = parse_libgen_html(libgen_html)
		download_libgen_book(book_title, file_type, valid_hash, key)

	elif provider == 'libraryLOL':
		print('Library LOL')

	else:
		print('no provider found')


if __name__ == '__main__':
	main()