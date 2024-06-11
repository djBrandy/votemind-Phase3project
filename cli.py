import sqlite3
from getpass import getpass
from models import initialize_db

DB_PATH = 'db/votemind.db'

def register():
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    identification_number = input("Enter identification number: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password, identification_number) VALUES (?, ?, ?)", 
                       (username, password, identification_number))
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("Username or identification number already exists!")
    finally:
        conn.close()

def login():
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    identification_number = input("Enter identification number: ")

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
        print("Invalid username, password, or identification number!")
        return None

def view_candidates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, party FROM candidates")
    candidates = cursor.fetchall()
    conn.close()

    if candidates:
        print("Candidates:")
        for candidate in candidates:
            print(f"{candidate[0]}. {candidate[1]} ({candidate[2]})")
    else:
        print("No candidates found.")

def vote(user_id):
    view_candidates()
    candidate_id = int(input("Enter the candidate ID to vote for: "))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO votes (user_id, candidate_id) VALUES (?, ?)", (user_id, candidate_id))
        conn.commit()
        print("Vote recorded successfully!")
    except sqlite3.IntegrityError:
        print("You have already voted!")
    finally:
        conn.close()

def endorse(user_id):
    view_candidates()
    candidate_id = int(input("Enter the candidate ID to endorse: "))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO endorsements (user_id, candidate_id) VALUES (?, ?)", (user_id, candidate_id))
        conn.commit()
        print("Endorsement recorded successfully!")
    finally:
        conn.close()

def add_candidate():
    name = input("Enter candidate name: ")
    party = input("Enter candidate party: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO candidates (name, party) VALUES (?, ?)", (name, party))
    conn.commit()
    conn.close()

    print("Candidate added successfully!")

def main():
    initialize_db()
    user_id = None
    print("Welcome to Votemind!")
    
    # Initial prompt for registration or login
    while user_id is None:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register()
        elif choice == '2':
            user_id = login()
        elif choice == '3':
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")
    
    # Main menu after successful login
    while True:
        print("\n1. View Candidates\n2. Vote\n3. Endorse\n4. Add Candidate\n5. Logout\n6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_candidates()
        elif choice == '2':
            vote(user_id)
        elif choice == '3':
            endorse(user_id)
        elif choice == '4':
            add_candidate()
        elif choice == '5':
            user_id = None
            print("Logged out successfully!")
            # Go back to the initial prompt for registration or login
            while user_id is None:
                print("\n1. Register\n2. Login\n3. Exit")
                choice = input("Enter your choice: ")

                if choice == '1':
                    register()
                elif choice == '2':
                    user_id = login()
                elif choice == '3':
                    print("Goodbye!")
                    return
                else:
                    print("Invalid choice. Please try again.")
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
