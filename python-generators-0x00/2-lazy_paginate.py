
import mysql.connector

def connect_to_prodev():
    """Connects to ALX_prodev database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="ALX_prodev"
    )


def paginate_users(page_size, offset):
    """Fetches a page of users starting from the given offset."""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """Generator that lazily fetches pages of users."""
    offset = 0

    while True:  # ✅ only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break  # stop when no more results
        yield page  # ✅ yield one page at a time
        offset += page_size  # move to next page
