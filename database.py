import sqlite3

class DBMS:

    def __init__(self, name):
        self.__name = name
        self.__connection = sqlite3.connect(self.__name)

    def __enter__(self):
        return self.__connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__connection.commit()
        self.__connection.close()


class BookstoreDB:

    def __init__(self, name: str) -> None:
        self.__name = name

    def create(self, isbn: int, title: str, author: str, edition: int, price: float, publisher: str) -> None:
        """
        Creates a book record
        :param isbn: int isbn
        :param title: str title
        :param author: str author
        :param edition: int edition
        :param price: float price
        :param publisher: str publisher
        :return: None
        """
        with DBMS(self.__name) as db:
            db.execute("""INSERT INTO Books (ISBN, Title, Author, Edition, Price, Publisher)
                          VALUES(?, ?, ?, ?, ?, ?)""", (isbn, title, author, edition, price, publisher))

    def read(self, isbn: int) -> tuple:
        """
        Queries book record for given isbn
        :param isbn: int isbn of book to be read
        :return: tuple book record
        """
        with DBMS(self.__name) as db:
            db.execute("SELECT * FROM Books WHERE ISBN == ?", (isbn,))
            result = db.fetchone()
            return result

    def update(self, isbn: int, title: str, author: str, edition: int, price: float, publisher: str) -> None:
        """
        Updates book record for given isbn
        :param isbn: int isbn of book to update
        :param title: str updated title for book
        :param author: str updated author for book
        :param edition: int updated edition
        :param price: float updated price
        :param publisher: str updated publisher
        :return: None
        """
        with DBMS(self.__name) as db:
            db.execute("""UPDATE Books
                       SET Title = ?,
                       Author = ?,
                       Edition = ?,
                       Price = ?,
                       Publisher = ?
                       WHERE ISBN == ?""", (title, author, edition, price, publisher, isbn))

    def delete(self, isbn) -> None:
        """
        Deletes book record for given isbn
        :param isbn: int isbn of book record to delete
        :return: None
        """
        with DBMS(self.__name) as db:
            db.execute("DELETE FROM Books WHERE ISBN == ?", (isbn,))

    def get_titles(self) -> list:
        """
        Gets a list of all titles from the database, with their __isbns
        :return: list[str] of all titles
        """
        with DBMS(self.__name) as db:
            db.execute("SELECT Title, ISBN FROM Books ORDER BY Title")
            result = db.fetchall()
            return result
