import sqlite3  # Importing the sqlite3 module to interact with a SQLite database
from getpass import getpass  # Importing the getpass module to securely handle password inputs
from models import initialize_db  # Importing the initialize_db function from your models.py file

DB_PATH = 'db/votemind.db'  # Setting the path to your SQLite database file

# Function to register a new user
def register():
    username = input("Enter username: ")  # Prompting the user to enter their username
    password = getpass("Enter password: ")  # Securely prompting the user to enter their password
    identification_number = input("Enter identification number: ")  # Prompting the user to enter their identification number

    conn = sqlite3.connect(DB_PATH)  # Connecting to your SQLite database
    cursor = conn.cursor()  # Creating a cursor object to execute SQL commands

    try:
        # Inserting the new user's details into the users table in your database
        cursor.execute("INSERT INTO users (username, password, identification_number) VALUES (?, ?, ?)", 
                       (username, password, identification_number))
        conn.commit()  # Committing the changes to the database
        print("User registered successfully!")  # Informing the user that their registration was successful
    except sqlite3.IntegrityError:
        # Informing the user that their chosen username or identification number already exists in the database
        print("Username or identification number already exists!")
    finally:
        conn.close()  # Closing the connection to the database

# Function to log in a user
def login():
    username = input("Enter username: ")  # Prompting the user to enter their username
    password = getpass("Enter password: ")  # Securely prompting the user to enter their password
    identification_number = input("Enter identification number: ")  # Prompting the user to enter their identification number

    conn = sqlite3.connect(DB_PATH)  # Connecting to your SQLite database
    cursor = conn.cursor()  # Creating a cursor object to execute SQL commands
    # Checking if the entered username, password, and identification number match any entry in the users table
    cursor.execute("SELECT id FROM users WHERE username=? AND password=? AND identification_number=?", 
                   (username, password, identification_number))
    user = cursor.fetchone()  # Fetching the first row of the results

    conn.close()  # Closing the connection to the database

    if user:
        print("Login successful!")  # Informing the user that their login was successful
        return user[0]  # Returning the user's ID
    else:
        # Informing the user that their entered username, password, or identification number is invalid
        print("Invalid username, password, or identification number!")
        return None  # Returning None

# Function to view all candidates
def view_candidates():
    conn = sqlite3.connect(DB_PATH)  # Connecting to your SQLite database
    cursor = conn.cursor()  # Creating a cursor object to execute SQL commands
    cursor.execute("SELECT id, name, party FROM candidates")  # Selecting all candidates from the candidates table
    candidates = cursor.fetchall()  # Fetching all rows of the results
    conn.close()  # Closing the connection to the database

    if candidates:
        print("Candidates:")  # Printing a header for the list of candidates
        for candidate in candidates:
            # Printing each candidate's ID, name, and party
            print(f"{candidate[0]}. {candidate[1]} ({candidate[2]})")
    else:
        print("No candidates found.")  # Informing the user that no candidates were found

# Function to vote for a candidate
def vote(user_id):
    view_candidates()  # Displaying all candidates
    candidate_id = int(input("Enter the candidate ID to vote for: "))  # Prompting the user to enter the ID of the candidate they want to vote for

    conn = sqlite3.connect(DB_PATH)  # Connecting to your SQLite database
    cursor = conn.cursor()  # Creating a cursor object to execute SQL commands

    try:
        # Inserting the user's vote into the votes table
        cursor.execute("INSERT INTO votes (user_id, candidate_id) VALUES (?, ?)", (user_id, candidate_id))
        conn.commit()  # Committing the changes to the database
        print("Vote recorded successfully!")  # Informing the user that their vote was recorded successfully
    except sqlite3.IntegrityError:
        print("You have already voted!")  # Informing the user that they have already voted
    finally:
        conn.close()  # Closing the connection to the database

# Function to endorse a candidate
def endorse(user_id):
    view_candidates()  # Displaying all candidates
    candidate_id = int(input("Enter the candidate ID to endorse: "))  # Prompting the user to enter the ID of the candidate they want to endorse

    conn = sqlite3.connect(DB_PATH)  # Connecting to your SQLite database
    cursor = conn.cursor()  # Creating a cursor object to execute SQL commands

    try:
        # Inserting the user's endorsement into the endorsements table
        cursor.execute("INSERT INTO endorsements (user_id, candidate_id) VALUES (?, ?)", (user_id, candidate_id))
        conn.commit()  # Committing the changes to the database
        print("Endorsement recorded successfully!")  # Informing the user that their endorsement was recorded successfully
    finally:
        conn.close()  # Closing the connection to the database

# Function to add a new candidate
def add_candidate():
    name = input("Enter candidate name: ")  # Prompting the user to enter the candidate's name
    party = input("Enter candidate party: ")  # Prompting the user to enter the candidate's party

    conn = sqlite3.connect(DB_PATH)  # Connecting to your SQLite database
    cursor = conn.cursor()  # Creating a cursor object to execute SQL commands
    # Inserting the new candidate's details into the candidates table
    cursor.execute("INSERT INTO candidates (name, party) VALUES (?, ?)", (name, party))
    conn.commit()  # Committing the changes to the database
    conn.close()  # Closing the connection to the database

    print("Candidate added successfully!")  # Informing the user that the candidate was added successfully

# Main function to run the application
def main():
    initialize_db()  # Initializing the database
    user_id = None  # Initializing the user_id variable to None
    print("Welcome to Votemind!")  # Printing a welcome message
    
    # Initial prompt for registration or login
    while user_id is None:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")  # Prompting the user to enter their choice

        if choice == '1':
            register()  # Registering a new user
        elif choice == '2':
            user_id = login()  # Logging in a user
        elif choice == '3':
            print("Goodbye!")  # Exiting the application
            return
        else:
            print("Invalid choice. Please try again.")  # Informing the user that their choice was invalid
    
    # Main menu after successful login
    while True:
        print("\n1. View Candidates\n2. Vote\n3. Endorse\n4. Add Candidate\n5. Logout\n6. Exit")
        choice = input("Enter your choice: ")  # Prompting the user to enter their choice

        if choice == '1':
            view_candidates()  # Viewing all candidates
        elif choice == '2':
            vote(user_id)  # Voting for a candidate
        elif choice == '3':
            endorse(user_id)  # Endorsing a candidate
        elif choice == '4':
            add_candidate()  # Adding a new candidate
        elif choice == '5':
            user_id = None  # Logging out the user
            print("Logged out successfully!")  # Informing the user that they have been logged out
            # Go back to the initial prompt for registration or login
            while user_id is None:
                print("\n1. Register\n2. Login\n3. Exit")
                choice = input("Enter your choice: ")  # Prompting the user to enter their choice

                if choice == '1':
                    register()  # Registering a new user
                elif choice == '2':
                    user_id = login()  # Logging in a user
                elif choice == '3':
                    print("Goodbye!")  # Exiting the application
                    return
                else:
                    print("Invalid choice. Please try again.")  # Informing the user that their choice was invalid
        elif choice == '6':
            print("Goodbye!")  # Exiting the application
            break
        else:
            print("Invalid choice. Please try again.")  # Informing the user that their choice was invalid

if __name__ == "__main__":
    main()  # Running the main function when the script is run directly
