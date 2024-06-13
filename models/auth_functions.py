# Importing sqlite3 module for database operations and getpass for secure password input
import sqlite3
from getpass import getpass

# Setting the path of the database
DB_PATH = 'db/votemind.db'

# User class to handle the user related operations
class User:
    # Function to register a new user
    def register(self):
        # Taking inputs for user details
        username = input("Enter username: ")
        password = getpass("Enter password: ")

        # Loop until a valid Kenyan identification number is entered
        while True:
            identification_number = input("Enter identification number: ")
            if identification_number.isdigit() and len(identification_number) == 8:
                break
            else:
                print("Enter a valid Kenyan identification number. Please ensure that you are an adult and an ID holder!")

        # Connecting to the database and executing the INSERT query
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, identification_number) VALUES (?, ?, ?)", 
                           (username, password, identification_number))
            conn.commit()
            print(f"{username} registered successfully, login to continue!")
        except sqlite3.IntegrityError:
            print("Username or identification number already exists! Log in to continue.")
        finally:
            conn.close()

    # Function to login a user
    def login(self):
        # Taking inputs for user details
        username = input("Enter username to continue: ")
        password = getpass("Enter password to continue: ")
        identification_number = input("Enter your identification number: ")

        # Connecting to the database and executing the SELECT query
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=? AND password=? AND identification_number=?", 
                       (username, password, identification_number))
        user = cursor.fetchone()
        conn.close()

        # Checking if the user exists and returning the user id
        if user:
            print("Login successful!")
            return user[0]
        else:
            print("Invalid username, password, or identification number! Also, try checking your spelling.")
            return None

# Admin class inherited from User class to handle the admin related operations
class Admin(User):
    # Admin code for admin login
    ADMIN_CODE = "AAQWAJZAMQW"

    # Function to login an admin
    def admin_login(self):
        # Taking input for admin code
        code = input("Enter admin code: ")

        # Checking if the entered code is correct
        if code == self.ADMIN_CODE:
            print("Admin login successful!")
            return True
        else:
            print("LOCKED!")
            return False