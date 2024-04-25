# import os

# web_server_path = os.path.dirname(__file__)
# books = '/var/www/html/books'
books = books.sort()


def update_site(book_cover):
	with open('index.html') as html_file:
		html_file.write(f'book\n')
		html_file.write(f'<a>')
		html_file.write(f'<img src="{book_cover}"')


# to place book in html, parse through html first find html tag then save as variable