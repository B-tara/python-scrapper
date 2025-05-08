
#  python -m pip install requests
# => get data from web (Html, json, xml)
# python -m pip install beautifulsoup4
# => parse html
# website ma data herna bhanako Get ho
# website ma data halna bhanako pass ho

# git:

# go to git bash
# git config --global user.name "Tara Bhandari"
# git config --global user.email " ..."

# git init => initialize git repository
# git status => if you want to check what are the status of files
# git diff => check what are the changes
# git add . => track all files from current directory
# git commit -m "your message"
# copy paste git ccode from github

##################################################################
# change the code
# git add .
# git commit -m "message"
# git push
##################################################################



import requests
from bs4 import BeautifulSoup
import sqlite3

url = 'https://books.toscrape.com/'


def create_table():
    con = sqlite3.connect("books.sqlite3")
    cursor = con.cursor()
    cursor.execute(
        """
        create table if not exists books (
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
    con = sqlite3.connect("books.sqlite3")
    cursor = con.cursor()
    cursor.execute(
        "insert into books (title, currency, price) values (?, ?, ?)",
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

    for book in book_elements:
        title = book.h3.a['title']
        # print(title)

        price_text = book.find ("p", class_ = 'price_color').text
        # print(price_text, type(price_text))
        currency = price_text[0]
        price = float(price_text[1:])
        # print(title, currency, price)

        insert_book(title, currency, price) # this code is written at last

    print("All data scrapped and saved to the database")

create_table()
scrape_book (url)

