from bs4 import BeautifulSoup

def add_cover_and_title(html_file, cover_path, title, link):
    # Default width and height for the image
    width = "50"
    height = "60"

    # Read the HTML file
    with open(html_file, "r") as file:
        html_content = file.read()

    # Parse the HTML content
    library = BeautifulSoup(html_content, "html.parser")

    # Find the list element where you want to add the new items
    list_element = library.find("ul", id="books")

    # Create a new <li> tag to contain both cover and title
    new_item = library.new_tag("li")

    # Create a new <img> tag for the cover
    new_img = library.new_tag("img", src=cover_path, width=width, height=height)
    new_item.append(new_img)

    # Create a new <a> tag for the title with link
    new_a = library.new_tag("a", href=link)
    new_a.string = title
    new_item.append(new_a)

    # Append the <li> tag to the <ul> tag
    list_element.append(new_item)

    # Append a newline character after the new item
    list_element.append("\n")

    # Write the modified HTML content back to the file
    with open(html_file, "w") as file:
        file.write(str(library))

# Example usage:
add_cover_and_title("library.html", "imgs/test.jpg", "Book Title", "https://example.com/book")