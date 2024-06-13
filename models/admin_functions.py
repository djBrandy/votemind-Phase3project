# Importing sqlite3 module for database operations
import sqlite3

# Setting the path of the database
DB_PATH = 'db/votemind.db'

# AdminFunctions class to handle the admin related operations
class AdminFunctions:
    # Function to add a new candidate
    def add_candidate(self):
        # Taking inputs for candidate details
        first_name = input("Enter candidate first name: ")
        last_name = input("Enter candidate last name: ")
        party = input("Enter candidate party: ")
        description = input("Enter candidate description: ")
        image_url = input("Enter candidate image URL: ")
        history = input("Enter candidate history: ")

        # Connecting to the database and executing the INSERT query
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO candidates (first_name, last_name, party, description, image_url, history) VALUES (?, ?, ?, ?, ?, ?)", 
                       (first_name, last_name, party, description, image_url, history))
        conn.commit()
        conn.close()

        print("Candidate added successfully!")

    # Function to update an existing candidate
    def update_candidate(self):
        # Taking inputs for candidate details
        candidate_id = int(input("Enter the candidate ID to update: "))
        first_name = input("Enter new first name: ")
        last_name = input("Enter new last name: ")
        party = input("Enter new party: ")
        description = input("Enter new description: ")
        image_url = input("Enter new image URL: ")
        history = input("Enter new history: ")

        # Connecting to the database and executing the UPDATE query
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE candidates SET first_name=?, last_name=?, party=?, description=?, image_url=?, history=? WHERE id=?", 
                       (first_name, last_name, party, description, image_url, history, candidate_id))
        conn.commit()
        conn.close()

        print("Candidate updated successfully!")

    # Function to delete a candidate
    def delete_candidate(self):
        # Taking input for candidate ID
        candidate_id = int(input("Enter the candidate ID to delete: "))

        # Connecting to the database and executing the DELETE query
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM candidates WHERE id=?", (candidate_id,))
        conn.commit()
        conn.close()

        print("Candidate deleted successfully!")

    # Function to view the number of registered candidates
    def view_registered_candidates(self):
        # Connecting to the database and executing the SELECT query
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM candidates")
        count = cursor.fetchone()[0]
        conn.close()

        print(f"Total number of registered candidates: {count}")

    # Function to view the number of users who have voted
    def view_users_voted(self):
        # Connecting to the database and executing the SELECT query
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM votes")
        count = cursor.fetchone()[0]
        conn.close()

        print(f"Total number of users who have voted: {count}")

    # Function to view the history of a candidate
    def view_candidate_history(self):
        # Taking input for candidate ID
        candidate_id = int(input("Enter the candidate ID to view history: "))
        
        # Connecting to the database and executing the SELECT query
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT history FROM candidates WHERE id=?", (candidate_id,))
        history = cursor.fetchone()
        conn.close()
        
        # Printing the history if found
        if history:
            print(f"Candidate History:\n{history[0]}")
        else:
            print("No history found for this candidate.")