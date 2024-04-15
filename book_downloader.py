import requests
import json
# from tqdm import tqdm
# TODO progress bar

def isbn_info(isbn: str):
	# returns books title for given isbn
	url = 'https://openlibrary.org/search.json?isbn='

	try:
		response = requests.get(url + isbn)
		response.raise_for_status()  # Raise an exception for bad status codes
		book_info = response.json()
		book_title = book_info["docs"][0]["title"]
		return book_title
	except requests.exceptions.RequestException as error:
		print(f'Error downloading HTML: {error}')
		return None


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
		print(f'Error downloading HTML: {error}')
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
	hashes = hashes[:10] # limit to 10 file hashes

	return hashes


def parse_anna_hashes(hashes: list):
	libgen_hashes = []
	libraryLOL_hashes = []
	file_type = ''
	file_extensions = ['.mobi', '.epub', '.pdf', '.lit', '.azw3', '.txt', '.cbz']
	libgen = 'http://libgen.li/ads.php?md5='
	libraryLOL = 'http://library.lol'

	for hsh in hashes:
		# download the html file for the file hash

		response = requests.get('https://annas-archive.org/md5/' + hsh)
		html_content = response.text

		for file_extension in file_extensions:
			if file_extension in html_content:
				file_type = file_extension

		# detecting download options
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

	return 'None', 'None', 'None'


def download_libgen_html(hsh: str):
	url = 'http://libgen.li/ads.php?md5='

	try:
		response = requests.get(url + hsh)
		response.raise_for_status()
		return response.text
	except requests.exceptions.RequestException as error:
		print(f'Error downloading HTML: {error}')
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
	print(url)
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
	response = requests.get(url, stream=True, headers=headers)

	if response.status_code == 200:
		print('connected')
		with open(book_title + file_type, 'wb') as file:
			file.write(response.content)
		print('File downloaded successfully')
	else:
		print('Failed to download file:', response.status_code)


# def download_libraryLOL_html:
		#TODO detect if fiction, fiction is fiction, nonfiction is main

# def parse_libraryLOL_html:



# ISBN = input("please enter the ISBN13 : ")
# print(f'entered {ISBN})
ISBN = '9780767908184'
BOOK_TITLE = isbn_info(ISBN)
#TODO, ask user if book title is correct, reprompt isbn if not
print(f'attempting to download : {BOOK_TITLE}')
ANNA_HTML = download_anna_html(ISBN)
HASHES = parse_anna_html(ANNA_HTML)
PROVIDER, VALID_HASH, FILE_TYPE = parse_anna_hashes(HASHES)
print(PROVIDER, VALID_HASH, FILE_TYPE)

if PROVIDER == 'libgen':
	LIBGEN_HTML = download_libgen_html(VALID_HASH)
	KEY = parse_libgen_html(LIBGEN_HTML)
	download_libgen_book(BOOK_TITLE, FILE_TYPE, VALID_HASH, KEY)

elif PROVIDER == 'libraryLOL':
	print('Library LOL')

else:
	print('no provider found')