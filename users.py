
import psycopg as pg


class Users:

    def __init__(self, conn: pg.Connection):
        self.conn = conn

    # methods specific to this class
    # check if user id already exists
    def check_user_id(self, userid: str):
        """
            Query to check if title exists
            :param conn: Connection to database
            :param title: title name
            :return: title
            """
        cmd = """SELECT
                      users.\"User-ID\"
                 FROM users
                 WHERE users.\"User-ID\" = %s"""
        cur = self.conn.cursor()
        cur.execute(cmd, (userid,))
        return False if cur.rowcount == 0 else True

    # Question 4
    def insert_user(self,
                    userid: int,
                    location: str,
                    age: int):
        """
        Query to insert a new user
        :param conn: Connection to database
        :param userid: id of user
        :param location: location of user
        :param age: age of user
        :return: inserts query to database
        """
        cmd = """INSERT INTO users (\"User-ID\", \"Location\", \"Age\")
                        VALUES (%s, %s, %s)"""
        cur = self.conn.cursor()
        cur.execute(cmd, (userid, location, age,))

