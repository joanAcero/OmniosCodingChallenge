from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://books.toscrape.com/index.html'

def get_page(url):
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
        title = book_element.find('h3').find('a').get('title') if book_element.find('h3') else None
        rating = book_element.find('p', class_="star-rating").get('class')[1] if book_element.find('p', class_="star-rating") else None
        price = book_element.find('p', class_="price_color").text if book_element.find('p', class_="price_color") else None
        picture = book_element.find('img').get('src') if book_element.find('img') else None

        titles.append(title)
        ratings.append(rating)
        prices.append(price)
        pictures.append(picture)

    return titles, ratings, prices, pictures


def get_all_pages_info(content):
    """
    Extracts information about all books on a given page and all subsequent pages.

    Parameters:
    - content (BeautifulSoup object): The HTML content of the page.

    Returns:
    Tuple of lists: Titles, ratings, prices, and picture URLs of all books on the page.
    """

    return [], [], [], []




if __name__ == "__main__":
    
    page_content = get_page(BASE_URL)
    

    titles, ratings, prices, pictures = get_all_pages_info(page_content)

    print('Titles:', titles)
    print('Ratings:', ratings)
    print('Prices:', prices)
    print('Pictures:', pictures)



