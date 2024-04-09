import requests

ANNAS = 'https://annas-archive.org/search?q="isbn13:9780062060617"'

ANNAS_PAGE = requests.get(ANNAS)

if ANNAS_PAGE.status_code == 200:
    print(ANNAS_PAGE.text)

# filter html for <a href="/md5/