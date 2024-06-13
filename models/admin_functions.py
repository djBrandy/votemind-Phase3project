import sqlite3

DB_PATH = 'db/votemind.db'

class AdminFunctions:
    def add_candidate(self):
        first_name = input("Enter candidate first name: ")
        last_name = input("Enter candidate last name: ")
        party = input("Enter candidate party: ")
        description = input("Enter candidate description: ")
        image_url = input("Enter candidate image URL: ")
        history = input("Enter candidate history: ")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO candidates (first_name, last_name, party, description, image_url, history) VALUES (?, ?, ?, ?, ?, ?)", 
                       (first_name, last_name, party, description, image_url, history))
        conn.commit()
        conn.close()

        print("Candidate added successfully!")

    def update_candidate(self):
        candidate_id = int(input("Enter the candidate ID to update: "))
        first_name = input("Enter new first name: ")
        last_name = input("Enter new last name: ")
        party = input("Enter new party: ")
        description = input("Enter new description: ")
        image_url = input("Enter new image URL: ")
        history = input("Enter new history: ")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE candidates SET first_name=?, last_name=?, party=?, description=?, image_url=?, history=? WHERE id=?", 
                       (first_name, last_name, party, description, image_url, history, candidate_id))
        conn.commit()
        conn.close()

        print("Candidate updated successfully!")

    def delete_candidate(self):
        candidate_id = int(input("Enter the candidate ID to delete: "))

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM candidates WHERE id=?", (candidate_id,))
        conn.commit()
        conn.close()

        print("Candidate deleted successfully!")

    def view_registered_candidates(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM candidates")
        count = cursor.fetchone()[0]
        conn.close()

        print(f"Total number of registered candidates: {count}")

    def view_users_voted(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM votes")
        count = cursor.fetchone()[0]
        conn.close()

        print(f"Total number of users who have voted: {count}")

    def view_candidate_history(self):
        candidate_id = int(input("Enter the candidate ID to view history: "))
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT history FROM candidates WHERE id=?", (candidate_id,))
        history = cursor.fetchone()
        conn.close()
        
        if history:
            print(f"Candidate History:\n{history[0]}")
        else:
            print("No history found for this candidate.")
