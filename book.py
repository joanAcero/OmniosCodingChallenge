class Book:

    current_id = 0 
    all_books = {}


    def __init__(self, title, review, price, imageUrl, id):
        self.title = title
        self.review = review
        self.price = price
        self.imageUrl = imageUrl

        self.id = Book.current_id
        Book.current_id += 1

        Book.all_books[self.id] = self

    def __str__(self):
        return f"Title: {self.title}, Review: {self.review}, Price: {self.price}, Image URL: {self.imageUrl}, ID: {self.id}"

    def get_all_books():
        return Book.all_books.values()


    
        