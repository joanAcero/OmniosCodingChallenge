import requests
from deep_translator import GoogleTranslator



class Book:
    
    #API_KEY = 'bda94d92-e99f-498f-aa15-8a10e257a44b'      Useless while there is no API provided!
    current_id = 0 
    all_books = {}


    def __init__(self, title, review, price, imageUrl, id):

        self.title = title
        self.review = review
        self.price = price
        self.imageUrl = imageUrl
        self.text = "" 
        self.spanishText = ""
        self.frenchText = ""
        self.eurosPrice = 0

        self.id = Book.current_id
        Book.current_id += 1

        Book.all_books[self.id] = self

    @staticmethod
    def get_all_books():
        '''Returns a list with all the books in the database.'''
        return Book.all_books.values()
    

    def generate_book_content(self):
        '''Generates the text of the book using an API.'''

        # query = ('The text of' + str(self.title) + 'is:')

        # r = requests.post("https://api.deepai.org/api/text-generator",
        # data={'text': query},
        # headers={'api-key': Book.API_KEY})
        # return r.json()

        #Dummy book content while the API is not provided!
        self.text = "The text of " + str(self.title) + " is:" 

    
    def translate_book_content(self):
        '''Translates the text of the book to Spanish and French.'''

        try:
            self.spanishText = GoogleTranslator(source='auto', target='es').translate(self.text)
            self.frenchText = GoogleTranslator(source='auto', target='fr').translate(self.text)
        except Exception as e:
            print(f"Translation error: {e} in the book {self.title}")
            self.spanishText = None  
            self.frenchText = None        
        

    def convert_price_to_euros(self,exchange_rate):
        '''Converts the price of the book from dollars to euros.'''
        self.eurosPrice = float(self.price) * exchange_rate
        

    def __str__(self):
        '''Change the behaviour of the str() function when applied to a Book object.'''

        return f"ID: {self.id}, Title: {self.title}, Review: {self.review}, Price: {self.price},Image URL: {self.imageUrl}, Text: {self.text}, Spanish Text: {self.spanishText}, French Text: {self.frenchText}, Euros Price: {self.eurosPrice}"
    




    
        