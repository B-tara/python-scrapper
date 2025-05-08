
#  python -m pip install requests
# python -m pip install beautifulsoup4
# website ma data herna bhanako Get ho
# website ma data halna bhanako pass ho

import requests
from bs4 import BeautifulSoup
import sqlite3

url = 'https://books.toscrape.com/'


def create_table():
    con = sqlite3.connect("books_1.sqlite3")
    cursor = con.cursor()
    cursor.execute(
        """
        create table if not exists books_1 (
            id integer primary key autoincrement,
            title text,
            currency text,
            price real
        )
    """
    )
    # con.commit()
    con.close()
    print("Database and table created successfully.")
    # pass

def insert_book(title, currency, price):
    con = sqlite3.connect("books_1.sqlite3")
    cursor = con.cursor()
    cursor.execute(
        "insert into books_1 (title, currency, price) values (?, ?, ?)",
        (title, currency, price),
    )
    con.commit()
    con.close()
    # pass

def scrape_book (url):
    response = requests.get(url)
    if response.status_code != 200:
        return
    
    # set encoding explicitly to handle special characters correctly
    response.encoding = response.apparent_encoding
    # print(response.text)

    soup = BeautifulSoup (response.text, "html.parser")
    book_elements = soup.find_all("article", class_ = "product_pod")
    #print (book_elements)

    books = []

    for book in book_elements:
        title = book.h3.a['title']
        # print(title)

        price_text = book.find ("p", class_ = 'price_color').text
        # print(price_text, type(price_text))
        currency = price_text[0]
        price = float(price_text[1:])
        # print(title, currency, price)

        insert_book(title, currency, price) # this code is written at last

        books_1.append (
            {
                "title": title,
                "currency": currency,
                "price": price,
            }
        )

    print("All data scrapped and saved to the database")
    return books_1

def save_to_json(books_1):
    import json

    with open ("books_1.json", "w", encoding="utf-8") as f:
        json.dump(books_1, f, indent=4, ensure_ascii=False)


def save_to_csv (books_1):
    import csv

    with open("books_1.csv", "w",newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "currency", "price"])
        writer.writeheader()
        writer.writer(books_1)

create_table()
books_1 = scrape_book(url)
save_to_json (books_1)
save_to_csv (books_1)

