import sqlite3
from db_init import DB_PATH

def add_candidate():
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

def view_candidate_history():
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
