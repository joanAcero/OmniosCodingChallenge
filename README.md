
# Omnios Coding Challenge

In the Omnios Coding Challenge, I was tasked with three primary objectives:

1 ) Scrape the provided website and for the books, get:

    - Title 
    - Star rating
    - Price
    - Picture URL 

2 ) Process : Complete previous data with the following params:

    - Generate an ID for each book.
    - Get the text of the book from this API*:
               The input text param should be like “The text of {title} is: “
    - Translate the field text into 2 popular languages.
    - Convert the price of the book to euros.

3 ) Store: Generate a file that contains all scraped data.


## Implementation

Firstly, to ensure the code is runnable on a maximum number of devices, I have Dockerized the project. You will find a Dockerfile in the project directory. More details on how to execute it are provided in the "Running with Docker" section.

In addition to the Dockerfile and the requirements.txt file, there are two other files in the project directory responsible for its implementation.

On one hand, main.py (the "core" file) executes, in its main function, the three tasks of the challenge using several functions.

On the other hand, the book.py file is responsible for creating the book class, which stores all the information of all books and completes the requested data with its functions.

At the end of the execution, all the information will be stored in the books.csv file. 

The code is modular and commented to enhance readability and facilitate changes, for example, in APIs.


## Running the code

To run the project, follow these steps:

1 ) Install Python (the latest version is recommended).

    $ sudo apt-get install python3.6


2 ) Open a terminal in the project directory.

3 ) Install the required libraries using the following command: 

    $ pip install -r requirements.txt

4 ) Execute the code by running: 

    $ python3 main.py


## Running with Docker

To execute the code using Docker without the need to install dependencies directly on your local machine, adhere to the steps outlined below.

1 ) Install Docker: Ensure Docker is installed on your machine. If not, you can download it from the official Docker website.


2 ) Open a Terminal: Open a terminal or command prompt in the project directory.

3 ) Build the Docker Image: Build the Docker image using the following command:

    $ docker build -t your-image-name:tag .

Replace your-image-name with the desired name for your image and tag with a version or tag for the image. The . at the end specifies the build context as the current directory.

4 ) Run the Docker Container: Run a container from the built image using:

    $ docker run -it your-image-name:tag

## Efficiency

The execution efficiency is tied to the performance of the utilized APIs, particularly in the context of the translation API and the text generation API.









