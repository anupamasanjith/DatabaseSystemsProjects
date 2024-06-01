import connect_books as cb
import tabulate as tb
from books import Books
from ratings import Ratings
from users import Users

def menu() -> str:
    """
    Present a menu to the user and return a valid option
    :return: 1, 2, Q, q
    """

    while True:
        print("1) Look up average rating by author")
        print("2) Look up average rating by title and author")
        print("3) Look up average rating of user with most reviews")
        print("4) Insert a new user")
        print("5) Insert a new book")
        print("6) Insert a new review")
        print("7) Get the authors with the most books published")
        print("8) Get the top n books by ratings")
        print("Q) Quit")
        opt = input("> ")
        if opt in ['1', '2', '3', '4', '5', '6', '7', '8', 'Q', 'q']:
            return opt
        else:
            print("Invalid option. Try again")
            break


if __name__ == "__main__":

    while True:
        conn = cb.connect()
        books = Books(conn)
        ratings = Ratings(conn)
        users = Users(conn)
        opt = menu()
        if opt == '1':
            inp = input("Enter author: ")
            if books.check_author(inp) == True:
                avg = ratings.get_avg_rating_by_author_name(inp)
                headers = ["Avg Rating", "Author name", "Newest Publication Year"]
                print(tb.tabulate(avg, headers, tablefmt="pretty"))
            else:
                print("Author not found. Please input valid author.")
                continue
            # if avg is None:
                # print("Author not found")
            # else:
                 # print(tb.tabulate(avg, headers, tablefmt="pretty"))
            conn.close()
        if opt == '2':
            # get rating by title and author
            # ask the user to enter a title and author
            title = input("Enter a title: ")
            # check if title exists
            if not books.check_title(title):
                print("Title not found. Please input valid title.")
                continue
            author = input("Enter the author: ")
            # check if author exists
            if not books.check_author(author):
                print("Author not found. Please input valid author.")
                continue
            rating = ratings.rating_by_title_author(title, author)
            if rating is None:
                print("No book found")
            else:
                print(rating)
            conn.close()
        elif opt == '3':
            # get average rating of user with most reviews
            user_rating = ratings.average_rating_most_reviews()
            print(user_rating)
            conn.close()
        elif opt == '4':
            try:
                userid = input("Enter user id: ")                # check if the user already exists
                if users.check_user_id(userid):
                    print("User already exists. Please input valid user id.")
                    continue
                location = input("Enter location: ")
                age = int(input("Enter age: "))
                user = users.insert_user(userid, location, age)
                print("User", userid, "entered.")
            except ValueError:
                print("Invalid entry.Try again")
                continue
        elif opt == '5':
            try:
                isbn = int(input("Enter isbn: "))
                # check if isbn already exists
                if books.check_isbn(isbn):
                    print("ISBN already exists. Please input valid isbn.")
                    continue
                else:
                # it is okay to have same title, author, etc. as long as the isbn does not already exist.
                    title = input("Enter book title: ")
                    author = input("Enter author name: ")
                    publishing_year = int(input("Enter publishing year: "))
                    publisher = input("Enter publisher: ")
                    book = books.insert_book(isbn, title, author, publishing_year, publisher)
                    print("Book", title, "entered.")

            except ValueError:
                print("Invalid entry.Try again")
                continue
        elif opt == '6':
            try:
                userid = int(input("Enter Userid: "))
                # check that user already exists before they can create a review
                if not users.check_user_id(userid):
                    print("User does not exist. Please input valid userid.")
                    continue
                isbn = input("Enter isbn: ")
                # check that the isbn exists to make sure it is a real book
                if not books.check_isbn(isbn):
                    print("ISBN does not exist. Please input valid isbn.")
                    continue
                rating = int(input("Enter rating: "))
                review = ratings.insert_review(userid, isbn, rating)
                print("Review entered")
            except ValueError:
                print("Invalid input. Try again")
                continue
        elif opt == '7':
            # get authors with the most books published
            try:
                n = int(input("Enter the amount of authors you want to see: "))
                if n > 0:
                    authors = Books.top_n_author(n)
                    headers = ['Author', 'Number of Books']
                    print(tb.tabulate(authors, headers))
                else:
                    print("Invalid amount. Try again")
                    continue

                conn.close()
            except ValueError:
                print("Invalid amount. Try again")
                continue
        elif opt == '8':
            try:
                n = int(input("Enter n: "))
                if n > 0:
                    output = books.n_most_popular_book(n)
                    headers = ["Title", "Author name", "Number of Ratings"]
                    print(tb.tabulate(output, headers, tablefmt="pretty"))
                else:
                    print("Invalid n. Enter non negative integer")
                    continue

            except ValueError:
                print("Invalid n. Enter non negative integer")
                continue
        elif opt in ['Q', 'q']:
            break