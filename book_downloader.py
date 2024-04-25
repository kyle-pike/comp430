'''
Downloads books from libgen.li and library.lol
----------------------------------------------
1) enter ISBN
2) with ISBN, parses through annas-archive.org for available downloads
3) finds and downloads the book
'''

import requests
# from tqdm import tqdm
# TODO progress bar


def isbn_info(isbn: str):
	# returns books title for given isbn and cover image (binary)
	book_title = ''
	url = 'http://openlibrary.org/api/volumes/brief/isbn/'

	try:
		response = requests.get(url + isbn + '.json')
		response.raise_for_status()  # Raise an exception for bad status codes
		book_info = response.json()

		# filter through API's JSON data to obtain book title
		book_dict = book_info['records']
		for key, value in book_dict.items():
			book_dict = value['data']
			for key, value in book_dict.items():
				if key == 'title':
					book_title = value

			# filter through JSON to obtain book cover url
			for key, value in book_dict.items():
				if key == 'cover':
					for key, value in value.items():
						if key == 'large':
							book_cover_url = value

		return book_title, book_cover_url

	except requests.exceptions.RequestException as error:
		print(f'Error connecting to openlibrary.org : {error}')
		return None


def download_book_cover(book_title, book_cover_url):
	try:
		response = requests.get(book_cover_url, stream=True)
		response.raise_for_status()  # Raise an exception for bad status codes

		if response.status_code == 200:
			print(f'connected to url')

			with open(book_title + '.jpg', 'wb') as file:
				file.write(response.content)
			print(f'{book_title} downloaded')

		else:
			print(f'Failed to download book cover : {response.status_code}')

	except requests.exceptions.RequestException as error:
		print(f'Error connecting to {book_cover_url} : {error}')


def download_anna_html(isbn: str):
	# detect if user entered ISBN 10 or 13
	if len(isbn) == 13:
		url = 'https://annas-archive.org/search?q="isbn13:'
	else:
		url = 'https://annas-archive.org/search?q="isbn10:'

	try:
		response = requests.get(url + isbn)
		response.raise_for_status()  # Raise an exception for bad status codes
		return response.text  # Return the HTML content
	except requests.exceptions.RequestException as error:
		print(f'Error connecting to annas-archive.org : {error}')
		return None


def parse_anna_html(html_content: str):
	hashes = []
	hash_id = 'href="/md5/'
	html_content_strings = html_content.split()

	# filter through strings to obtain md5 file hashes
	for string in html_content_strings:
		if hash_id in string:
			string = string.split(hash_id)
			string = string[-1]
			string = string.split('"')
			string = string[0]
			hashes.append(string)
	hashes = hashes[:25] # limit to 25 file hashes

	return hashes


def parse_anna_hashes(hashes: list):
	libgen_hashes = []
	libraryLOL_hashes = []
	file_type = ''
	file_extensions = ['.mobi', '.epub', '.pdf', '.lit', '.azw3', '.txt', '.cbz']
	libgen = 'http://libgen.li/ads.php?md5='
	libraryLOL = 'http://library.lol'

	for hsh in hashes:
		# download the html file
		response = requests.get('https://annas-archive.org/md5/' + hsh)
		html_content = response.text

		# obtain the file extension
		for file_extension in file_extensions:
			if file_extension in html_content:
				file_type = file_extension

		# see if a download is available
		if (libgen + hsh) in html_content:
			libgen_hashes.append(hsh)
		elif libraryLOL in html_content:
			libraryLOL_hashes.append(hsh)
		else:
			print(f'no download options available for hash : {hsh}')

		# provide the first file hash with a download option
		if hsh in libgen_hashes:
			return 'libgen', hsh, file_type

		elif hsh in libraryLOL_hashes:
			return 'libraryLOL', hsh, file_type

	return None, None, None


def download_libgen_html(hsh: str):
	url = 'http://libgen.li/ads.php?md5='

	try:
		response = requests.get(url + hsh)
		response.raise_for_status()
		return response.text
	except requests.exceptions.RequestException as error:
		print(f'Error connecting to libgen.li : {error}')
		return None


def parse_libgen_html(html_content: str):
	key_id = '&key='
	key = ''
	html_content_list = html_content.split()

	# filter through strings to obtain key
	for strings in html_content_list:
		if key_id in strings:
			strings = strings.split(key_id)
			strings = strings[-1]
			strings = strings.split('"')
			strings = strings[0]
			key = strings
	return key


def download_libgen_book(book_title, file_type, hsh, key):
	url = 'http://libgen.li/get.php?md5=' + hsh + '&key=' + key
	print(f'download url : {url}')
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

	try:
		response = requests.get(url, stream=True, headers=headers)
		response.raise_for_status()  # Raise an exception for bad status codes

		if response.status_code == 200:
			print(f'connected to url')

			with open(book_title + file_type, 'wb') as file:
				file.write(response.content)
			print(f'{book_title} downloaded')

		else:
			print(f'Failed to download from libgen : {response.status_code}')

	except requests.exceptions.RequestException as error:
		print(f'Error connecting to libgen : {error}')


def download_libraryLOL_html(hsh):
	response = requests.get('https://annas-archive.org/md5/' + hsh)
	html_content = response.text
	html_content_lines = html_content.split('\n')
	libraryLOL = '<a href="http://library.lol/'
	download_url = ''

	# filter to obtain download link
	for line in html_content_lines:
		if libraryLOL in line:
			line = line.split()
			line = line[1]
			line = line.split('"')
			download_url = line[1]

	try:
		response = requests.get(download_url)
		response.raise_for_status()
		return response.text
	except requests.exceptions.RequestException as error:
		print(f'Error connecting to library.lol : {error}')
		return None


def download_libraryLOL_book(book_title, file_type, html_content):
	url = ''

	# filter through strings to obtain download link
	for line in html_content.split('\n'):
		if 'https://download.library.lol/' in line:
			line = line.split('"')
			url = line[1]

	print(f'download url : {url}')

	# attempt to download book
	try:
		response = requests.get(url, stream=True)
		response.raise_for_status()  # Raise an exception for bad status codes

		if response.status_code == 200:
			print('connected to url')

			with open(book_title + file_type, 'wb') as file:
				file.write(response.content)
			print(f'{book_title} downloaded')

		else:
			print(f'Failed to download from library.lol : {response.status_code}')

	except requests.exceptions.RequestException as error:
		print(f'Error connecting to library.lol : {error}')


def download_book(isbn, book_title):
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