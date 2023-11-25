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

    def get_all_books():
        return Book.all_books
    
    def get_book_by_id(id):
        return Book.all_books[id]

    
        