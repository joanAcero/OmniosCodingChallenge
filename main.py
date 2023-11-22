from bs4 import BeautifulSoup
import requests

PAGE_URL = 'https://books.toscrape.com/index.html'

def get_page(url):
    """
    Fetches the content of a web page specified by the provided URL, using the requests library.
    If the request is successful, the HTML content is parsed using BeautifulSoup,
    and the prettified version of the HTML is returned.

    Parameters:
    - url (str): The URL of the web page to fetch.

    Returns:
    - str: The prettified HTML content of the web page.

    Raises:
    - requests.exceptions.HTTPError: If an HTTP error (4xx or 5xx) occurs during the request.
    - requests.exceptions.ConnectionError: If a connection error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_error:
        print(f"HTTP Error: {http_error}")
        # You can raise a custom exception here if needed
    except requests.exceptions.ConnectionError as connection_error:
        print(f"Connection Error: {connection_error}")
        # You can raise a custom exception here if needed

    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.prettify()

if __name__ == "__main__":
    page_content = get_page(PAGE_URL)
    
    
    if page_content:
        print(page_content)
    else:
        print("Failed to fetch and parse the HTML content.")
