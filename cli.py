import sqlite3
from getpass import getpass
from models import initialize_db, update_db_schema

DB_PATH = 'db/votemind.db'
ADMIN_CODE = "AAQWAJZAMQW"

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

def admin_login():
    code = input("Enter admin code: ")

    if code == ADMIN_CODE:
        print("Admin login successful!")
        return True
    else:
        print("Invalid admin code!")
        return False

def view_candidates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, first_name, last_name, party, description, image_url FROM candidates")
    candidates = cursor.fetchall()
    conn.close()

    if candidates:
        print("Candidates:")
        for candidate in candidates:
            print(f"{candidate[0]}. {candidate[1]} {candidate[2]} ({candidate[3]}) - {candidate[4]}")
            print(f"Image URL: {candidate[5]}\n")
    else:
        print("No candidates found.")

def view_votes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT candidates.id, candidates.first_name, candidates.last_name, candidates.party, 
           COUNT(votes.id) as vote_count
    FROM candidates
    LEFT JOIN votes ON candidates.id = votes.candidate_id
    GROUP BY candidates.id, candidates.first_name, candidates.last_name, candidates.party
    ''')
    results = cursor.fetchall()
    conn.close()

    if results:
        print("Vote Counts:")
        for result in results:
            print(f"{result[0]}. {result[1]} {result[2]} ({result[3]}) - {result[4]} votes")
    else:
        print("No votes found.")

def view_endorsements():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT candidates.id, candidates.first_name, candidates.last_name, candidates.party, 
           COUNT(endorsements.id) as endorsement_count,
           GROUP_CONCAT(endorsements.summary, '\n') as summaries
    FROM candidates
    LEFT JOIN endorsements ON candidates.id = endorsements.candidate_id
    GROUP BY candidates.id, candidates.first_name, candidates.last_name, candidates.party
    ''')
    results = cursor.fetchall()
    conn.close()

    if results:
        print("Endorsement Counts and Summaries:")
        for result in results:
            print(f"{result[0]}. {result[1]} {result[2]} ({result[3]}) - {result[4]} endorsements")
            print(f"Endorsement Summaries:\n{result[5]}")
    else:
        print("No endorsements found.")

def vote(user_id):
    view_candidates()
    candidate_id = int(input("Enter the candidate ID to vote for: "))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if the user has already voted
    cursor.execute("SELECT id FROM votes WHERE user_id=?", (user_id,))
    vote = cursor.fetchone()
    
    if vote:
        print("You have already voted!")
    else:
        try:
            cursor.execute("INSERT INTO votes (user_id, candidate_id) VALUES (?, ?)", (user_id, candidate_id))
            conn.commit()
            print("Vote recorded successfully!")
        except sqlite3.IntegrityError:
            print("An error occurred while recording your vote.")
        finally:
            conn.close()

def endorse(user_id):
    view_candidates()
    candidate_id = int(input("Enter the candidate ID to endorse: "))
    summary = input("Enter a short summary for your endorsement: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the user has already endorsed
    cursor.execute("SELECT id FROM endorsements WHERE user_id=?", (user_id,))
    endorsement = cursor.fetchone()

    if endorsement:
        print("You have already endorsed a candidate!")
    else:
        try:
            cursor.execute("INSERT INTO endorsements (user_id, candidate_id, summary) VALUES (?, ?, ?)", (user_id, candidate_id, summary))
            conn.commit()
            print("Endorsement recorded successfully!")
        except sqlite3.IntegrityError:
            print("An error occurred while recording your endorsement.")
        finally:
            conn.close()

def add_candidate():
    first_name = input("Enter candidate first name: ")
    last_name = input("Enter candidate last name: ")
    party = input("Enter candidate party: ")
    description = input("Enter candidate description: ")
    image_url = input("Enter candidate image URL: ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO candidates (first_name, last_name, party, description, image_url) VALUES (?, ?, ?, ?, ?)", 
                   (first_name, last_name, party, description, image_url))
    conn.commit()
    conn.close()

    print("Candidate added successfully!")

def main():
    initialize_db()
    update_db_schema()
    user_id = None
    admin_logged_in = False
    print("Welcome to Votemind!")
    
    while user_id is None and not admin_logged_in:
        print("\n1. Register\n2. Login\n3. Admin Login\n4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register()
        elif choice == '2':
            user_id = login()
        elif choice == '3':
            admin_logged_in = admin_login()
        elif choice == '4':
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")
    
    while True:
        if admin_logged_in:
            print("\n1. Add Candidate\n2. Logout\n3. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                add_candidate()
            elif choice == '2':
                admin_logged_in = False
                print("Logged out successfully!")
                user_id = None
                break
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            print("\n1. View Candidates\n2. View Votes\n3. View Endorsements\n4. Vote\n5. Endorse\n6. Logout\n7. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                view_candidates()
            elif choice == '2':
                view_votes()
            elif choice == '3':
                view_endorsements()
            elif choice == '4':
                vote(user_id)
            elif choice == '5':
                endorse(user_id)
            elif choice == '6':
                user_id = None
                print("Logged out successfully!")
                break
            elif choice == '7':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        
        while user_id is None and not admin_logged_in:
            print("\n1. Register\n2. Login\n3. Admin Login\n4. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                register()
            elif choice == '2':
                user_id = login()
            elif choice == '3':
                admin_logged_in = admin_login()
            elif choice == '4':
                print("Goodbye!")
                return
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
