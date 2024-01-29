from flask import Flask, render_template
from dotenv import load_dotenv
import os
import mysql.connector

app = Flask(__name__)

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE'),
    'port': int(os.getenv('DB_PORT')),
}


def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/")
def index():

    connection =get_db_connection()
    cursor = connection.cursor()

    # SQL statement to get all books
    select_query = '''
        SELECT * FROM books;
    '''

    cursor.execute(select_query)
    books = cursor.fetchall()
    connection.close()

    book_dict =[]
    keys = ["id", "title", "author", "published"]
    for book_list in books:
        book_values ={}
        for idx in range(4):
            if idx == 3:
                book_values[keys[idx]] = str(book_list[idx])[0:4]
            else:
                book_values[keys[idx]] =  book_list[idx]
        book_dict.append(book_values)

    return render_template("index.html", books = book_dict)
