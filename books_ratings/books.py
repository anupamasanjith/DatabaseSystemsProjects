
import psycopg as pg
import re

class Books:

    # Constructor
    def __init__(self, conn: pg.Connection):
        self.conn = conn

    # methods specific to the books table
    # clean up input text (in regard to punctuation, spacing, etc.)
    def clean_text(self,
                   name):
        """
        Cleans the author name
        :param name:
        :param author: author name
        :return: cleaned author name
        """
        return re.sub(r'[^A-Za-z0-9]+', '', name).strip().lower()

    # check if the author exists
    def check_author(self, author: str):
        """
        Query to check if author exists
        :param conn: Connection to database
        :param author: author name
        :return: author
        """

        cleaned_author = self.clean_text(author)
        cmd = """SELECT
                      books.\"Book-Author\"
                 FROM books
                 WHERE LOWER(REGEXP_REPLACE(books.\"Book-Author\", E'[^A-Za-z0-9]+', '', 'g')) = %s"""
        cur = self.conn.cursor()
        cur.execute(cmd, (cleaned_author,))
        return False if cur.rowcount == 0 else True

    # check if title exists
    def check_title(self, title: str):
        """
            Query to check if title exists
            :param conn: Connection to database
            :param title: title name
            :return: title
            """
        cmd = """SELECT
                      books.\"Book-Title\"
                 FROM books
                 WHERE books.\"Book-Title\" = %s"""
        cur = self.conn.cursor()
        cur.execute(cmd, (title,))
        return False if cur.rowcount == 0 else True

    # check if ISBN exists
    def check_isbn(self, isbn: int):
        """
            Query to check if isbn exists
            :param conn: Connection to database
            :param isbn: isbn of book
            :return: isbn
            """
        cmd = """SELECT
                      books.isbn
                 FROM books
                 WHERE books.isbn = %s"""
        cur = self.conn.cursor()
        cur.execute(cmd, (isbn,))
        return False if cur.rowcount == 0 else True

    # Question 5
    def insert_book(self,
                    isbn: str,
                    title: str,
                    author: str,
                    publishing_year: int,
                    publisher: str):
        """
        Query to insert a new user
        :param conn: Connection to database
        :param isbn: isbn of book
        :param title: title of book
        :param author: author name
        :param publishing_year: year of publishing
        :param publisher: publisher name
        :return: inserts new user
        """
        cmd = """INSERT INTO books (isbn, \"Book-Title\", \"Book-Author\", \"Year-Of-Publication\", \"Publisher\")
                        VALUES (%s, %s, %s, %s, %s)"""

        cur = self.conn.cursor()
        cur.execute(cmd, (isbn, title, author, publishing_year, publisher,))


    # Question 7
    def top_n_author(self, n: int):
        """
        Gets the top n authors with the highest amount of books published
        :param conn:
        :param n: input by user
        :return: top n authors
        """
        cmd = """SELECT
                    \"Book-Author\",
                    count(\"Book-Author\") as num_books
                    FROM
                        books
                    GROUP BY
                        \"Book-Author\"
                    ORDER BY
                        count(\"Book-Author\") DESC
                    LIMIT %s"""

        cur = self.conn.cursor()
        cur.execute(cmd, [n])

        rv = []
        for row in cur:
            rv.append(row)
        if cur.rowcount == 0:
            return None
        cur.close()
        return rv

    # Question 8
    def n_most_popular_book(self,
                            n: int):
        """
        Query to find n most popular books by number of ratings
        :param conn: Connection to Database
        :param n: Number of Books
        :return: n number of titles,authors and total number of ratings
        """
        cmd = """SELECT
                      b.\"Book-Title\",
                      b.\"Book-Author\",
                      COUNT(r.\"Book-Rating\") AS number_of_ratings
                 FROM
                     books AS b
                 LEFT JOIN ratings AS r ON b.isbn = r.isbn
                 GROUP BY b.\"Book-Title\", b.\"Book-Author\"
                 ORDER BY number_of_ratings DESC
                 LIMIT %s;"""

        cur = self.conn.cursor()
        cur.execute(cmd, (n,))

        return None if cur.rowcount == 0 else cur.fetchall()


