from book_downloader import *
# from display import *
# from input import *

def main():

	'''
	----- PROCESS -----
	1) LCD : enter ISBN
	2) * user enters isbn via pin pad or scanner *
		function that deletes or backspace if messed up ISBN via pin pad
	3) LCD : $ISBN, request another?
	4) * user inputs more ISBNs or presses key on pin pad to finish *

	5) LCD : grabs status from book_downloader.py, ex: downloading $book_title
		attempting to download $book_title
		found available download / did not find available download
		downloading (progress bar)

	6) LCD : finished, please obtain books via $URL
	7) LCD : return to start?
	restarts process
	'''

	# while inputting is True:

	books = {}

	# for isbn, book_title in books:
	isbn = '9780813054964'
	book_title, book_cover_url = isbn_info(isbn)
	download_book_cover(book_title, book_cover_url)
	print(f'attempting to download : {book_title}')
	download_book(isbn, book_title)


if __name__ == '__main__':
	main()