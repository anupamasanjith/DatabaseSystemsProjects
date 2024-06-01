
import psycopg as pg
from books import Books
from users import Users
import re


class Ratings:

    def __init__(self, conn: pg.Connection):
        self.conn = conn

    # methods specific to this class

    def clean_text(self,
                   name):
        """
        Cleans the author name
        :param name:
        :param author: author name
        :return: cleaned author name
        """
        return re.sub(r'[^A-Za-z0-9]+', '', name).strip().lower()

    # Question 1
    def get_avg_rating_by_author_name(self,
                                      author: str):
        """
        Query to find authors average book rating
        :param conn: Connection to database
        :param author: author name
        :return: average rating,Number of books written
        and Newest Publication Year
        """
        # Injection attack possible
        # Injection attack possible where '{cleaned_author}' is used instead of a parameter. A user could enter another SQL query command and
        # comment out the rest of your code. This would allow them to run any SQL command they want.
        cleaned_author = self.clean_text(author)
        cmd = f""" SELECT
                         ROUND(AVG(subquery.AvgRating), 1) AS AvgRating,
                         SUM(subquery.NumberOfBooks) AS TotalNumberOfBooks,
                          MAX(subquery.NewestPublicationYear) AS OverallNewestPublicationYear
                    FROM(
                        SELECT
                             ROUND(AVG(ratings.\"Book-Rating\"),1) AS AvgRating,
                             COUNT(books.isbn) AS NumberOfBooks,
                             MAX(\"Year-Of-Publication\") AS NewestPublicationYear
                         FROM
                            books
                         LEFT JOIN
                            ratings ON books.isbn = ratings.isbn
                         WHERE
                            LOWER(REGEXP_REPLACE(books.\"Book-Author\", E'[^A-Za-z0-9]+', '', 'g')) = '{cleaned_author}'
                         GROUP BY
                            books.\"Book-Author\") AS subquery"""
        cur = self.conn.cursor()
        cur.execute(cmd, )

        return None if cur.rowcount == 0 else cur.fetchall()

    # Question 2
    def rating_by_title_author(self,
                               title: str,
                               author: str) -> int | None:
        """
        Gets the rating of a book based on the title and author
        :param conn:
        :param title:
        :param author:
        :return: rating
        """
        # Select the average book rating
        clean_author = self.clean_text(author)
        cmd = """SELECT
                    ROUND(avg(\"Book-Rating\")) as avg_rating, \"Book-Title\", \"Book-Author\"
                  FROM
                    (SELECT
                        \"Book-Rating\",
                        \"Book-Title\",
                        \"Book-Author\"
                     FROM
                        books JOIN ratings ON ratings.isbn = books.isbn) as T
                  WHERE
                    \"Book-Title\" = %s and LOWER(REGEXP_REPLACE(\"Book-Author\", E'[^A-Za-z0-9]+', '', 'g')) = %s
                  GROUP BY
                        \"Book-Title\",
                        \"Book-Author\""""

        # Get a cursor to execute the theory
        cur = self.conn.cursor()
        cur.execute(cmd, [title, clean_author])

        # get the resultset which is either of size zero or one
        rv = None
        if cur.rowcount > 0:
            rv = cur.fetchone()[0]
        cur.close()
        return rv

    # Question 3
    def average_rating_most_reviews(self):
        """
        Gets the average rating of the user with the most reviews
        :param conn:
        :return: rating
        """

        # Select the average book rating
        cmd = """SELECT
                    avg(\"Book-Rating\") as avg_rating, \"User-ID\"
                 FROM
                    (SELECT
                        \"Book-Rating\",
                        \"User-ID\"
                     FROM
                        books JOIN ratings ON ratings.isbn = books.isbn) as T
                    GROUP BY
                        \"User-ID\"
                    ORDER BY
                        count(\"User-ID\") DESC
                    LIMIT 1"""

        cur = self.conn.cursor()
        cur.execute(cmd, )

        # get the resultset which is either of size zero or one
        rv = None
        if cur.rowcount > 0:
            rv = cur.fetchone()[0]
        cur.close()
        return rv

    # Question 6
    def insert_review(self,
                      userid: int,
                      isbn: str,
                      rating: int):
        """
        Query to insert new review
        :param conn: Connection to Database
        :param userid: id of user
        :param isbn: isbn of book
        :param rating: rating by user
        :return: inserts new review
        """
        cmd = """INSERT INTO ratings (\"User-ID\", "isbn", \"Book-Rating\")
                        VALUES (%s, %s, %s)"""
        cur = self.conn.cursor()
        cur.execute(cmd, (userid, isbn, rating,))

