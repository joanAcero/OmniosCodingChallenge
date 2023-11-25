import requests

class Book:
    
    API_KEY = 'bda94d92-e99f-498f-aa15-8a10e257a44b'
    current_id = 0 
    all_books = {}


    def __init__(self, title, review, price, imageUrl, id):
        self.title = title
        self.review = review
        self.price = price
        self.imageUrl = imageUrl

        self.id = Book.current_id
        Book.current_id += 1

        self.text = Book.generate_book_content(title)

        Book.all_books[self.id] = self

    def __str__(self):
        return f"Title: {self.title}, Review: {self.review}, Price: {self.price}, Image URL: {self.imageUrl}, ID: {self.id}, Text: {self.text}"

    def get_all_books():
        return Book.all_books.values()
    

    def generate_book_content(self):

        query = ('The text of' + str(self.title) + 'is:')

        r = requests.post("https://api.deepai.org/api/text-generator",data={'text': query},headers={'api-key': Book.API_KEY})

        return r.json()




    
        