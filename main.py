from bs4 import BeautifulSoup
import requests

from book import Book

FIRST_PAGE = 'page-1.html'
BASE_URL = 'https://books.toscrape.com/catalogue/'


def get_next_page_url(content):
    """
    Finds the URL of the next page, if it exists.

    Parameters:
    - content (BeautifulSoup object): The HTML content of the page.

    Returns:
    - next_page_url (str): The URL of the next page, if it exists.
    """

    next_page_url = content.find('li', class_="next").find('a').get('href') if content.find('li', class_="next") else None
    next_page_url = (BASE_URL + next_page_url) if next_page_url else None

    return next_page_url


def get_page_html(url):
    """
    Fetches the content of a web page specified by the provided URL, using the requests library.
    If the request is successful, the HTML content is parsed using BeautifulSoup,
    and the HTML is returned.

    Parameters:
    - url (str): The URL of the web page to fetch.

    Returns:
    - soup (BeautifulSoup object): The HTML content of the page.

    Raises:
    - requests.exceptions.HTTPError: If an HTTP error (4xx or 5xx) occurs during the request.
    - requests.exceptions.ConnectionError: If a connection error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error: {http_error}")
    except requests.exceptions.ConnectionError as connection_error:
        print(f"Connection Error: {connection_error}")

    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def new_book_object(title, rating, price, picture, id):
    """
    Creates a new Book object.

    Parameters:
    - title (str): The title of the book.
    - rating (str): The rating of the book.
    - price (str): The price of the book.
    - picture (str): The URL of the picture of the book.
    - id (int): The ID of the book.
    """
    Book(title, rating, price, picture, id)

    
def get_book_info(book_content):
    """
    Extracts information about a book from its HTML content and creates a Book object.

    Parameters:
    - book_content (BeautifulSoup object): The HTML content of the book.

    Returns:
    Tuple of strings: Title, rating, price, and picture URL of the book.
    """

    title = book_content.find('h3').find('a').get('title') if book_content.find('h3') else None
    rating = book_content.find('p', class_="star-rating").get('class')[1] if book_content.find('p', class_="star-rating") else None
    price = book_content.find('p', class_="price_color").text if book_content.find('p', class_="price_color") else None
    picture = book_content.find('img').get('src') if book_content.find('img') else None

    # Create a Book object for each book and append it to the books list.
    new_book_object(title, rating, price, picture, None)

    return title, rating, price, picture


def get_page_info(content):
    """
    Extracts information about each book on a given page.

    Parameters:
    - content (BeautifulSoup object): The HTML content of the page.

    Returns:
    Tuple of lists: Titles, ratings, prices, and picture URLs of all books on the page.
    """

    titles = []
    ratings = []
    prices = []
    pictures = []

    # Find all book elements identified by <li></li> tag and class = col-xs-6 col-sm-4 col-md-3 col-lg-3 in the HTML of the page.
    book_elements = content.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    # For each book element, extract the title, rating, price, and picture URL and append this information to its respective lists.
    for book_element in book_elements:
        title, rating, price, picture = get_book_info(book_element)

        titles.append(title)
        ratings.append(rating)
        prices.append(price)
        pictures.append(picture)

    return titles, ratings, prices, pictures


def get_all_pages_info(page_content):
    """
    Extracts information about all books on a given page and all subsequent pages.

    Parameters:
    - content (BeautifulSoup object): The HTML content of the page.

    Returns:
    Tuple of lists: Titles, ratings, prices, and picture URLs of all books on the page.
    """

    all_titles = []
    all_ratings = []
    all_prices = []
    all_pictures = []

    current_page_content = page_content

    # While there is a next page, fetch its content and extract the information about the books on it.
    while current_page_content:

        #Get the titles, ratings, prices and picture URL of the books of the current page.
        titles, ratings, prices, pictures = get_page_info(page_content)

        all_titles.extend(titles)
        all_ratings.extend(ratings)
        all_prices.extend(prices)
        all_pictures.extend(pictures)

        # Find the URL of the next page, if it exists.
        next_page_url = get_next_page_url(current_page_content)

        # If the next page exists, fetch its content and repeat the process.
        current_page_content = get_page_html(next_page_url) if next_page_url else None

    return all_titles, all_ratings, all_prices, all_pictures


def complete_data():
    books = Book.get_all_books()

    for book in books: 

        book.generate_book_content()
        book.translate_book_content()
        book.convert_price_to_euros()


if __name__ == "__main__":

    #1 ) Scrape the provided website and for the books get the title, rating, price and picture URL.
    base_page_content = get_page_html(BASE_URL + FIRST_PAGE)
    
    titles, ratings, prices, pictures = get_all_pages_info(base_page_content)

    #2) Process: Complete the previous data. Generate a unique ID for each book, generate the text of the book, translate and convert the price to euros.

    complete_data()

    # Print the information about each book.
    for book in books: print(str(book) + "\n")





