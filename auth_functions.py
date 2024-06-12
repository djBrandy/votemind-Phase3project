import sqlite3
from getpass import getpass
from db_init import DB_PATH

def register():
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    while True:
        identification_number = input("Enter identification number: ")
        if identification_number.isdigit() and len(identification_number) == 8:
            break
        else:
            print("Enter a valid Kenyan identification number. please ensure that you are an adult and an ID holder!")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, identification_number) VALUES (?, ?, ?)", 
                       (username, password, identification_number))
        conn.commit()
        print(f"{username} registered successfully, login to continue! ")

    except sqlite3.IntegrityError:
        print("Username or identification number already exists! Log in to continue.")
    finally:
        conn.close()

def login():
    username = input("Enter username to continue: ")
    password = getpass("Enter password to continue: ")
    identification_number = input("Enter your identification number: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=? AND identification_number=?", 
                   (username, password, identification_number))
    user = cursor.fetchone()

    conn.close()

    if user:
        print("Login successful!")
        return user[0]
    else:
        print("Invalid username, password, or identification number! also try checking your spelling")
        return None

def admin_login():
    ADMIN_CODE = "AAQWAJZAMQW"
    code = input("Enter admin code: ")

    if code == ADMIN_CODE:
        print("Admin login successful!")
        return True
    else:
        print("LOCKED!")
        return False
