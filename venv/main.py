import csv
import sqlite3
import pytz
import datetime
import hashlib

db = sqlite3.connect("library.sqlite")

db.execute("CREATE TABLE IF NOT EXISTS members"
                "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "username TEXT UNIQUE NOT NULL,"
                "password TEXT NOT NULL,"
                "role TEXT NOT NULL)")

db.execute("CREATE TABLE IF NOT EXISTS books"
                "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "title TEXT NOT NULL,"
                "author TEXT NOT NULL,"
                "genre TEXT,"
                "ISBN INTEGER UNIQUE NOT NULL,"
                "no_of_copies INTEGER NOT NULL)")

db.execute("CREATE TABLE IF NOT EXISTS transactions"
           "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
           "user_id INTEGER,"
           "book_id INTEGER,"
           "borrow_date TEXT,"
           "due_date TEXT,"
           "FOREIGN KEY(user_id) REFERENCES members(id),"
           "FOREIGN KEY(book_id) REFERENCES books(id))")


class User(object):

    def __init__(self, username, password, role = 'Member'):
        self._username = username
        self.__password = self.hash_password(password)
        self._role = role

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.__password == self.hash_password(password)

    def get_role(self):
        return self._role
    
    def get_password(self):
        return self.__password



class Admin(User):

    def __init__(self, username, password):
        super().__init__(username, password, role='Admin') 


    def insert_into_db(self):

        try:
            db.execute("INSERT INTO members (username, password, role) VALUES (?, ?, ?)", (self._username, self.get_password(), self._role ))
            db.commit()
            print(f"Admin {self._username} Registered successfully!.")

        except sqlite3.IntegrityError as e:
            print(f"Error: Admin {self._username} already exists.: {e}")
        except Exception as e:
            print(f"Error: {e}")

    
    def add_member(self, username, password):

        try:
            member = Member(username, password)
            db.execute("INSERT INTO members (username, password, role) VALUES (?, ?, ?)", (member._username, member.get_password(), member._role))
            db.commit()
            print(f"Member {member._username} has been added successfully!")

        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")


    def delete_member(self, username):

        try:
            db.execute("DELETE FROM members WHERE username = ?", (username,))
            db.commit()
            print(f"Member {username} has been removed!")
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    
    def update_member(self,new_username, new_password, username):

        try:
            db.execute("UPDATE members SET username = ?, password = ? WHERE username = ?",(new_username, new_password, username))
            db.commit()
            print(f"Member {username}'s information updated successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    
    def show_all_members(self):

        try:
            cursor = db.execute("SELECT * FROM members")
            users_info = cursor.fetchall()
            print(f"{'ID':<5} {'Name':<15} {'Role':<12}")
            
            for users in users_info:
                id, name, passw, role = users
                print(f"{id:<5} {name:<15} {role:<12}")
        except sqlite3.IntegrityError as e:
            print(f"Error finding members!: {e}")
        except Exception as e:
            print(f"Error: {e}")


    def add_book_from_library(self, library, book):
      
        library.addBook_to_BookList(book)
        print(f"Book {book._title} has been added to the Book list!")

        try:
            cursor = db.execute("SELECT * FROM books WHERE title = ? AND ISBN = ?", (book._title, book._Isbn))
            book_info = cursor.fetchone()

            if book_info is None:
                db.execute("INSERT INTO books (title, author, genre, ISBN, no_of_copies) VALUES (?, ?, ?, ?, ?)", (book._title, book._author, book._genre, book._Isbn, book.no_of_copies))
                db.commit()
                print(f"Book {book._title} has been added successfully to the database!")
            else:
                library.deleteBook_from_BookList(book)
                print(f"Book {book._title} already exists!")

        except sqlite3.IntegrityError as e:
           library.deleteBook_from_BookList(book)
           print(f"Error during adding book {book._title}: {e}")
        except Exception as e:
            print(f"Error: {e}")


    def delete_book(self, library, book_title):

        book_to_remove = None
        book_list = library.get_bookList()

        for book in book_list:
            if book._title.lower() == book_title.lower():
                book_to_remove = book
                break


        if book_to_remove:
            try:
                cursor = db.execute("SELECT * FROM books WHERE title = ?", (book_title,))
                book_info = cursor.fetchone()

                if book_info is None:
                    print(f"Book {book_title} was not found in database!")
                else:
                    db.execute("DELETE FROM books WHERE title = ?", (book_title,))
                    db.commit()
                    print(f"Book {book_title} removed successfully from database!")

                    library.deleteBook_from_BookList(book_to_remove)
                    print(f"Book {book_title} removed from book list also!")

            except sqlite3.IntegrityError as e:
                library.addBook_to_BookList(book_to_remove)
                print(f"Error during deletion of book {book_title}: {e}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"Book {book_title} was not found in book list!")

   

    def update_book_info(self, library, book_title):

        book_to_update = None
        book_list = library.get_bookList()

        for book in book_list:
            if book._title == book_title:
                book_to_update = book
                break
        
        if book_to_update:
            try:
                cursor = db.execute("SELECT * FROM books WHERE title = ?", (book_title,))
                book_info = cursor.fetchone()

                if book_info is None:
                    print(f"Book {book_title} was not found")
                else:
                    id, title, author, genre, Isbn, no_of_copies = book_info

                    title2 = str(input("Enter new title of the book: "))
                    author2 = str(input("Enter new author name: "))
                    genre2 = str(input("Enter new genre type: "))
                    no_of_copies2 = int(input("Enter new no. of copies: "))

                    db.execute("UPDATE books SET title = ?, author = ?, genre = ?, ISBN = ?, no_of_copies = ? WHERE title = ?", (title2, author2, genre2, Isbn, no_of_copies2, title))
                    db.commit()
                    print(f"Book {book_title}'s information updated successfully!")

                    book_to_update._title = title2
                    book_to_update._author = author2
                    book_to_update._genre = genre2
                    book_to_update.no_of_copies = no_of_copies2
                    print(f"Book {book_title}'s information updated in book list also!")

            except sqlite3.IntegrityError as e:
                print(f"Error during updating book {book_title}: {e}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"Book {book_title} was not found in the book list!")


    def show_all_books(self):
        try:
            cursor = db.execute("SELECT * FROM books")
            book_info = cursor.fetchall()
            print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Genre':<18} {'ISBN':<18} {'No. of copies':<10}")
            for book in book_info:
                id,title, author, genre, Isbn, no_of_copies = book
                print(f"{id:<5} {title:<30} {author:<20} {genre:<18} {Isbn:<18} {no_of_copies:<10}")
        except sqlite3.IntegrityError as e:
            print(f"Error showing books!: {e}")
        except Exception as e:
            print(f"Error: {e}")

    
    def populate_books_from_csv(self, csv_path):
        try:
            csv_path = csv_path.strip()
            with open(csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        db.execute(
                            "INSERT INTO books (title, author, genre, ISBN, no_of_copies) VALUES (?, ?, ?, ?, ?)",
                            (row['Title'], row['Author'], row['Genre'], row['ISBN'], row['No_of_Copies'])
                        )
                        db.commit()
                        print(f"Book {row['Title']} added successfully!")
                    except sqlite3.IntegrityError as e:
                        print(f"Error inserting {row['Title']}: {e}")
        except FileNotFoundError as e:
            print(f"CSV file not found. Please check the file path.: {e}")
        except Exception as e:
            print(f"Error: {e}")
                


class Member(User):

    borrow_list = []
    return_list = []

    def __init__(self, username, password, role='Member'):
        super().__init__(username, password, role)
    
    @staticmethod
    def _current_date():
        bd_timezone = pytz.timezone('Asia/Dhaka')
        current_date = datetime.datetime.now(bd_timezone).date()
        return current_date
    
    def load_borrowed_books(self, member_id):

        Member.borrow_list.clear()
        try:
            cursor = db.execute("SELECT books.id, books.title, books.author, books.genre, books.ISBN, books.no_of_copies FROM transactions "
                                " INNER JOIN books ON transactions.book_id = books.id "
                                " WHERE transactions.user_id = ? AND transactions.due_date is not NULL", (member_id,))

            borrowed_books = cursor.fetchall()

            if not borrowed_books :
                print("Borrow list is empty!")
            else:
                print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Genre':<18} {'ISBN':<18}")
                for book in borrowed_books:
                    id, title, author, genre, Isbn, no_of_copies = book
                    book = Book(title, author, genre, Isbn, no_of_copies)
                    Member.borrow_list.append((id, book))
        
        except sqlite3.IntegrityError as e:
            print(f"Error: loading books-{e}")
        except Exception as e:
            print(f"Error: {e}")


    def search_books(self, book_choice):
        valid_genres = ['Fiction', 'Fantasy', 'Romance', 'Historical', 'Dystopian', 'Science Fiction', 'Cyber Punk', 'Horror', 'Drama', 'Satire']
                                
        if book_choice in valid_genres:

            try:
                cursor = db.execute("SELECT * FROM books WHERE genre = ?", (book_choice,))
                book_info = cursor.fetchall()

                if len(book_info) == 0:
                    print(f"Sorry, no result found for genre {book_choice}!")
                else:
                    print(f"Available Books for genre {book_choice}:")
                    print(f"{'ID':<5} {'Title':<40} {'Author':<35} {'Genre':<18} {'ISBN':<18} {'Copies':<5}")

                    for book in book_info:
                        id, title, author, genre, Isbn, no_of_copies = book
                        print(f"{id:<5} {title:<40} {author:<35} {genre:<18} {Isbn:<18} {no_of_copies:<5}")
            except sqlite3.IntegrityError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Try different keywords!")


    def borrow_books(self, book_id, member_id):

        book_borrow_limit = 3
        try:
            if len(Member.borrow_list) >= book_borrow_limit:
                print(f"You have reached your borrow limit of {book_borrow_limit} books. Please return a book to borrow more.")
                return
            
            cursor = db.execute("SELECT * FROM books WHERE id = ?", (book_id,))
            book_info = cursor.fetchone()

            if book_info is None:
                print(f"Book with ID {book_id} is not available right now!")
            else:
                id, title, author, genre, Isbn, no_of_copies = book_info
                
                print(f"Book found with ID {id}")
                print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Genre':<18} {'ISBN':<18} {'No. of copies':<10}")
                print(f"{id:<5} {title:<30} {author:<20} {genre:<18} {Isbn:<18} {no_of_copies:<10}")

                if no_of_copies > 0:
                    cursor = db.execute("SELECT * FROM transactions WHERE user_id = ? AND book_id = ? AND due_date is not NULL", (member_id, book_id))

                    if cursor.fetchone() is not None:
                        print(f"Sorry, you have already borrowed this book")
                        return
                    
                    no_of_copies -= 1
                    db.execute("UPDATE books SET no_of_copies = ? WHERE id = ?", (no_of_copies, book_id))
                    db.commit()
                    print(f"Number of copies of book {title} updated!")

                    borrow_date = self._current_date()
                    due_date = borrow_date + datetime.timedelta(days=7)

                    db.execute("INSERT INTO transactions (user_id, book_id, borrow_date, due_date) VALUES (?, ?, ?, ?)", (member_id, book_id, borrow_date, due_date))
                    db.commit()
                    print(f"Borrow successful..")

                    book = Book(title, author, genre, Isbn, no_of_copies)
                    Member.borrow_list.append((id, book))

                    print(f"You borrowed Book {title} on {borrow_date}, Please return it within {due_date}")
                    print("Thank you for borrowing this book, it's a great book to read. Happy Reading!")
                
                else:
                    print("Sorry, no copies available!")
        
        except sqlite3.IntegrityError as e:
            print(f"Error during borrowing book with ID {book_id}: {e}")
        except Exception as e:
            print(f"Error: {e}")



    def return_books(self, book_id, member_id):

        book_return = None
        for id, book in Member.borrow_list:
            if id == book_id:
                book_return = book
                break
            
        if book_return:
            try:  
                cursor = db.execute("SELECT * FROM transactions WHERE book_id = ? AND user_id = ? AND due_date is not NULL", (book_id, member_id))
                transaction_info = cursor.fetchone()

                if not transaction_info:
                    print("Sorry, you have no book to return!")
                else:
                    id, u_id, b_id, borrow_date, due_date, return_date = transaction_info
                    today = self._current_date()
                    due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d').date()

                    if today <= due_date:
                        print(f"You borrowed this book with ID {book_id} on {borrow_date}")

                        cursor = db.execute("SELECT no_of_copies FROM books WHERE id = ?", (book_id,))
                        book_info = cursor.fetchone()

                        if not book_info:
                            print(f"Book info with ID {book_id} was not found!")
                        else:
                            no_of_copies = book_info[0]
                            no_of_copies += 1
                            
                            db.execute("UPDATE books SET no_of_copies = ? WHERE id = ?", (no_of_copies, book_id))
                            db.execute("UPDATE transactions SET due_date = NULL, return_date = ? WHERE book_id = ? AND user_id = ?", (today, book_id, member_id))
                            db.commit()

                            Member.borrow_list.remove((book_id, book_return))
                            Member.return_list.append((book_id, book_return))
                            print(f"Book with ID {book_id} has been returned and number of copies updated!")
                    else:
                        print(f"You are returning this book late!")
            
            except sqlite3.IntegrityError as e:
                print(f"Error during returning book with ID {book_id}: {e}")
            except Exception as e:
                print(f"Error! exception occurred: {e}")
        else:
            print(f"You did not borrow any book with ID {book_id}")


    def show_all_books(self):

        print("Available Books: ")
        try:
            cursor = db.execute("SELECT * FROM books")
            book_info = cursor.fetchall()

            print(f"{'ID':<5} {'Title':<40} {'Author':<25} {'Genre':<18} {'ISBN':<18} {'No. of copies':<10}")
            for book in book_info:
                id,title, author, genre, Isbn, no_of_copies = book
                print(f"{id:<5} {title:<40} {author:<25} {genre:<18} {Isbn:<18} {no_of_copies:<10}")
        except sqlite3.IntegrityError as e:
            print(f"Error showing books!: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def show_borrowList(self, member_id, member_name):

        try:
            print("Borrow List: ")
            self.load_borrowed_books(member_id)

            for id, book in Member.borrow_list: 
                        print(f"{id:<5} {book._title:<30} {book._author:<20} {book._genre:<18} {book._Isbn:<18}")

            print(f"Loaded {len(Member.borrow_list)} books in borrow list for member {member_name} with ID {member_id}")
        except sqlite3.IntegrityError as e:
            print(f"Error: showing borrowlist- {e}")
        except Exception as e:
            print(f"Error: {e}")    



class Library(object):

    book_list = []

    def load_books_from_db(self):
        try:
            cursor = db.execute("SELECT * FROM books")
            books_from_db = cursor.fetchall()

            for book_data in books_from_db:
                id, title, author, genre, Isbn, no_of_copies = book_data
                book = Book(title, author, genre, Isbn, no_of_copies)
                self.addBook_to_BookList(book)  
            print(f"Loaded {len(Library.book_list)} books from the database.")
        except sqlite3.IntegrityError as e:
            print(f"Error loading books from the database!: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def addBook_to_BookList(self, book):
        Library.book_list.append(book)
    
    def deleteBook_from_BookList(self, book):
        Library.book_list.remove(book)
    
    def get_bookList(self):
        return Library.book_list
    

class Book(object):

    def __init__(self, title, author, genre, Isbn, no_of_copies):
        self._title = title
        self._author = author
        self._genre = genre
        self._Isbn = Isbn
        self.no_of_copies = no_of_copies
     
    
choice = None
if __name__ == '__main__':

    library = Library()
    library.load_books_from_db()

    option1 = {'1': 'Registration', '2': 'Login', '0': 'Exit'}
    option2 = {'1': "Add Member", '2': "Delete Member", '3': "Update member info", '4': "Show all members", '5': 'Add Book', '6': "Delete Book", '7': "Update Book", '8': "Show all books",'9': "Populate books from csv", '0': 'Exit'}
    option3 = {'1': "Search Books",'2': "Show all books", '3': "Borrow book", '4': "Return book",'5': "Show Borrow List",'6': "Show Return List", '0': "Exit"}
    admin = None
    
    while True:
        print("----Welcome to the Libarary Mangement System----")
        for x, y in option1.items():
            print(f"{x}.  {y}")

        choice = input("Choose an option: ")
        if choice == '1':
            username = input("Please enter your username: ")
            password = input("Enter your password: ")

            admin = Admin(username, password)
            admin.insert_into_db()
        
        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            cursor = db.execute("SELECT * FROM members WHERE username = ?", (username,))
            user_info = cursor.fetchone()

            if user_info is None:
                print(f"User {username} not found!")
            else:
                user_id, uname, hash_passw, role = user_info
                
                if role == 'Admin':
                    user = Admin(uname, hash_passw)
                else:
                    user = Member(uname, hash_passw)

                hashed_password = user.hash_password(password)
                if user.check_password(hashed_password):
                    if user.get_role() == 'Admin':

                        print(f"Login successful! Welcome, {uname}")
                        while True:
                            print("-------------------------------")
                            print("----------ADMIN PANEL----------")
                            print("-------------------------------")
                            for x, y in option2.items(): 
                                print(f"{x}.  {y}")

                            choice2 = input("Choose an option: ") 
                            if choice2 == '1':
                                member_name = input("Enter member name: ")
                                member_pass = input("Enter password: ")
                                user.add_member(member_name, member_pass)

                            elif choice2 == '2':
                                member_to_remove = input("Enter member name to remove: ")
                                user.delete_member(member_to_remove)

                            elif choice2 == '3':
                                user_name_toUpdate = input("Enter member name to update: ")

                                try:
                                    cursor = db.execute("SELECT * FROM members WHERE username = ?", (user_name_toUpdate,))
                                    user_info = cursor.fetchone()

                                    if user_info is None:
                                        print("User not found!")
                                    else:
                                        user_id, uname, hash_passw, role = user_info

                                        if user_name_toUpdate == uname:
                                            old_password = input("Enter existing password: ")
                                            hashed_old_password = user.hash_password(old_password)

                                            if hashed_old_password == hash_passw:
                                                new_username = input("Enter member's new name: ")
                                                new_password = input("Enter new password: ")
                                                re_new_password = input("Re-enter new password: ")

                                                if new_password == re_new_password:
                                                    hashed_new_password = user.hash_password(new_password)
                                                    user.update_member(new_username, hashed_new_password, user_name_toUpdate)
                                                else:
                                                    print("Password should match!")
                                            else:
                                                print("password incorrect!")
                                        else:
                                            print(f"{user_name_toUpdate} didn't match!")
                                except sqlite3.IntegrityError as e:
                                    print(f"Error: {e}")
                                except Exception as e:
                                    print(f"Error: {e}")

                            elif choice2 == '4':
                                user.show_all_members()
        
                            elif choice2 == '5':

                                title = str(input("Please enter the title of the book: "))
                                author = str(input("Enter the author name: "))
                                genre = str(input("Enter genre type: "))
                                Isbn = int(input("Enter ISBN number: "))
                                no_of_copies = int(input("Enter no. of copies: "))

                                book = Book(title, author, genre, Isbn, no_of_copies)
                                user.add_book_from_library(library, book)
                                
                            elif choice2 == '6':
                              
                                book_to_remove = str(input("Enter book name to remove: "))
                                user.delete_book(library, book_to_remove)
                                
                            elif choice2 == '7':

                                book_to_update = input("Enter book name to update: ")
                                user.update_book_info(library, book_to_update)

                            elif choice2 == '8':
                                user.show_all_books()

                            elif choice2 == '9':
                                csv_path = input("Enter the path to your CSV file: ").strip()
                                user.populate_books_from_csv(csv_path)

                            elif choice2 == '0':
                                break
                    
                        
                    elif user.get_role() == 'Member':
                        
                        print("Login successful.")
                        print(f"Welcome, {uname}")

                        while True:
                            print(f"{uname}'s Panel---------")

                            for key, value in option3.items():
                                print(f"{key}.   {value}")

                            choice3 = input("Choose an option: ")
                            if choice3 == '1':

                                print(f"Try searching with these keyword:\n `Fiction`, `Fantasy`, `Romance`, `Historical`, `Dystopian`, `Science Fiction`, `Cyber Punk`, `Horror`")
                                book_choice = str(input("Enter genre name to find books available: "))
                                user.search_books(book_choice)
            
                            elif choice3 == '2':
                                user.show_all_books()

                            elif choice3 == '3':
                                book_to_borrow = int(input("Enter book ID to borrow: "))
                                user.borrow_books(book_to_borrow, user_id)

                            elif choice3 == '4':
                                book_to_return = int(input("Enter book ID to return: "))
                                user.return_books(book_to_return, user_id)

                            elif choice3 == '5':
                                user.show_borrowList(user_id, uname)

                            elif choice3 == '0':
                                break

                            else:
                                print("Invalid option...")
                else:
                    print("Incorrect Password.")
        elif choice == '0':
            break
        else:
            print("Invalid choice!")
    
    db.close()