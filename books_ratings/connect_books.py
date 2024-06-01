import psycopg as pg


# question 1
# 4,5,6
# try 7 & 8

def connect() -> pg.Connection:
    """
    Return a connection object to the books database or exit if failure
    :return: connection object
    """

    # What can go wrong?
    try:
        pwd_file = open("/Users/anupamasanjith/.pwd")
    except OSError as e:
        print(f"Error: File not readable,{e}")
        exit()

    password = pwd_file.readline().strip()

    try:

        # connect with an existing database
        conn = pg.connect(
            dbname="jeff_and_lupi_booksdataset",
            host="ada.hpc.stlawu.edu",
            user="asanj19",
            password=password
        )
    except pg.Error as e:
        print(f"Error: could not connect to database {e}")
        exit()
    finally:
        pwd_file.close()

    return conn
