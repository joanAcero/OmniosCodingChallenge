from bs4 import BeautifulSoup
import requests
import csv
from forex_python.converter import CurrencyRates
from tqdm import tqdm

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
        soup = BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error: {http_error}")
        soup = None
    except requests.exceptions.ConnectionError as connection_error:
        print(f"Connection Error: {connection_error}")
        soup = None
    
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
    price = float((book_content.find('p', class_="price_color").text)[1:]) if book_content.find('p', class_="price_color") else None
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

    if not content: return titles, ratings, prices, pictures #take into account if the content is None ( because of an error getting the information of the page)

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

    print("Scraping...")
    progress_bar = tqdm(total=50, desc='Pages Scraped', position=0, leave=True)


    # For each page, extract the information about each book and append it to its respective list.
    for i in range(1,51):

        #Get the titles, ratings, prices and picture URL of the books of the current page.
        titles, ratings, prices, pictures = get_page_info(current_page_content)

        all_titles.extend(titles)
        all_ratings.extend(ratings)
        all_prices.extend(prices)
        all_pictures.extend(pictures)

        # Find the URL of the next page, if it exists.
        next_page_url = get_next_page_url(current_page_content)

        # If the next page exists, fetch its content and repeat the process.
        current_page_content = get_page_html(next_page_url) if next_page_url else (BASE_URL + 'page-' + str(i+1) + '.html')

        # Update the progress bar
        progress_bar.update(1)

    return all_titles, all_ratings, all_prices, all_pictures


def complete_data():
    """
    Completes the data of each book in the database.    
    """


    books = Book.get_all_books()

    print(str(len(books)) + " books scraped from the website, completing data...")

    try:
        exchange_rate = CurrencyRates().get_rate('USD', 'EUR')
    except Exception as e:
        print("Problem getting the current exchange rate. Exchange rate set to 0.91")
        exchange_rate = 0.91

    i = 1
    for book in tqdm(books):                                  # For each book in the database:                          
        
        book.generate_book_content()                    # Generate the text of the book using an API.
        book.convert_price_to_euros(exchange_rate)      # Convert the price of the book from dollars to euros.
        book.translate_book_content()                   # Translate the text of the book to Spanish and French.
        #print(f"Book {i} completed")                    # Print a message to the console to show the progress.
        i += 1


def generate_csv():
    """
    Generates a CSV file with all the scraped data.
    """

    books = Book.get_all_books()

    with open('books.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['ID', 'Title', 'Review', 'Price($)', 'Price(€)', 'Picture URL', 'Text', 'Spanish Text', 'French Text'])

        for book in books:
            writer.writerow([book.id, book.title, book.review, book.price, book.eurosPrice , book.imageUrl, book.text, book.spanishText, book.frenchText])


if __name__ == "__main__":

    #1 ) Scrape the provided website and for each books get the title, rating, price and picture URL.
    
    base_page_content = get_page_html(BASE_URL + FIRST_PAGE)
    
    titles, ratings, prices, pictures = get_all_pages_info(base_page_content)

    print("data scraped")

    #2) Process: Complete the previous data. Generate a unique ID for each book, generate the text of the book, translate and convert the price to euros.

    complete_data()

    print("data completed")
    
    #3)Store: Generate a file that contains all scraped data.
    
    generate_csv()




   





