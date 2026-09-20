import sqlite3

def initialize_table(cursor):
    """
    Initialize database table
    :param cursor: Cursor object used for interacting with database
    :return: None
    """
    # drop the table if it exists
    cursor.execute("DROP TABLE IF EXISTS Books")

    # create a Books table
    cursor.execute("""CREATE TABLE Books (ISBN INTEGER PRIMARY KEY NOT NULL,
                                          Title TEXT,
                                          Author TEXT,
                                          Edition INTEGER,
                                          Price REAL,
                                          Publisher TEXT)""")


def add_books(cursor):
    """
    Adds products to the database table
    :param cursor: Cursor object used for interacting with database
    :return: None
    """
    # create a list of books
    books = [(1234567891234, "Your Book", "Your Author", 1, 9.99, "Your Publisher")]

    # iterate over products list and insert values into Products table
    for isbn, title, author, edition, price, publisher in books:
        cursor.execute("""INSERT INTO Books (ISBN, Title, Author, Edition, Price, Publisher)
                          VALUES(?, ?, ?, ?, ?, ?)""", (isbn, title, author, edition, price, publisher))


def main():
    # create a connection
    connection = sqlite3.connect("bookstore.db")

    # create a cursor
    cursor = connection.cursor()

    # processes
    initialize_table(cursor)
    print("...\nTable successfully initialized.")

    # add books
    add_books(cursor)
    print("...\nBooks successfully added.")

    # commit changes
    connection.commit()
    print("...\nChanges successfully committed.")

    # close the connection
    connection.close()


if __name__ == '__main__':
    main()
