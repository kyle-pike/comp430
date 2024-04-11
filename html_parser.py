import requests


def download_anna_html(isbn: str):
	url = 'https://annas-archive.org/search?q="isbn13:'
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
	html_content_list = html_content.split()

	# filter through strings to obtain md5 file hashes
	for strings in html_content_list:
		if hash_id in strings:
			strings = strings.split(hash_id)
			strings = strings[-1]
			strings = strings.split('"')
			strings = strings[0]
			hashes.append(strings)
	return hashes[0]


def download_libgen_html(hsh: str):
	url = 'http://libgen.li/ads.php?md5='
	# for hsh in hashes:
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


def book_libgen(hsh, key):
	url = 'http://libgen.li/get.php?md5=' + hsh + '&key=' + key
	print(url)
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
	response = requests.get(url, headers=headers)

	if response.status_code == 200:
		print('connected')
		with open('book.epub', 'wb') as file:
			file.write(response.content)
		print('File downloaded successfully')
	else:
		print('Failed to download file:', response.status_code)


# ISBN = input("please enter ISBN13")
# print(ISBN)
# print(type(ISBN))
ANNA_HTML = download_anna_html('9780786838653')
HASHES = parse_anna_html(ANNA_HTML)
print(HASHES)
LIBGEN_HTML = download_libgen_html(HASHES)
KEY = parse_libgen_html(LIBGEN_HTML)
book_libgen(HASHES, KEY)