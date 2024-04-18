import os

# web_server_path = os.path.dirname(__file__)
# books = '/var/www/html/books'
books = books.sort()

with open(index.html, 'w') as html_file:
	for book in books:
		if book in html_file:
			pass
		else:
			html_file.write(f'book\n')


# to place book in html, parse through html first find html tag then save as variable