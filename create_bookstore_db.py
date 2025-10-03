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
    books = [(9781974718900, "Sensor", "Junji Ito", 3, 19.99, "Viz Media"),
             (1234567890123, "Debug", "Debug", 1, 9.99, "Debug"),
             (9780312558154, "The Dream of Perpetual Motion", "Dexter Palmer", 1, 24.99, "St. Martin's Press"),
             (9780761169086, "Atlas Obscura", "Joshua Foer", 1, 35.00, "Workman Publishing"),
             (9780385663250, "The Montreal Canadiens: 100 Years of Glory", "D'Arcy Jenish", 2, 22.00, "Anchor Canada"),
             (9780321546342, "This Book is Full of Spiders", "David Wong", 1, 25.99, "Thomas Dunne Books"),
             (9784805314432, "Japanese Death Poems", "Yoel Hoffman", 2, 14.99, "Tuttle Publishing"),
             (9781250318541, "Mistborn", "Brandon Sanderson", 2, 9.99, "Tor"),
             (9781250318572, "The Well of Ascension", "Brandon Sanderson", 2, 10.99, "Tor"),
             (9781250318626, "The Hero of Ages", "Brandon Sanderson", 2, 10.99, "Tor"),
             (9780593201275, "How to Sell a Haunted House", "Grady Hendrix", 2, 18.00, "Berkley")]


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
