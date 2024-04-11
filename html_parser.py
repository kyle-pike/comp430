import requests


def download_anna(isbn: str):
	url = 'https://annas-archive.org/search?q="isbn13:'
	try:
		response = requests.get(url + isbn)
		response.raise_for_status()  # Raise an exception for bad status codes
		return response.text  # Return the HTML content
	except requests.exceptions.RequestException as error:
		print(f"Error downloading HTML: {error}")
		return None


def parse_anna(html_content: str):
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
	return hashes[:3]


def download_libgen(hashes: str):


# a = download_anna('9780547951942')
# print(parse_anna(a))