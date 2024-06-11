# importing sql 
import sqlite3
# importing a python statement that ensures that the passwords that are being entered by the users are secure.
from getpass import getpass

from models import initialize_db, update_db_schema
# importing the pyplot from the library of matplotlib, and renaming it to plt for convenience.
# this is what enables users to have a view of the votes in a graph like manner.
import matplotlib.pyplot as plt


DB_PATH = 'db/votemind.db'
ADMIN_CODE = "AAQWAJZAMQW"

# creating a method that handles the functionality of registering users.
def register():
    # prompting the user to input the username, password, (and this is where getpass is being called) and identification number.
    username = input("Enter username: ")
    password = getpass("Enter password: ")
# remember to create a loop that is going to ensure that the identification is a number, and should only contain 8 characters, just like an id number.

    while True:
        identification_number = input("Enter identification number: ")
        if identification_number.isdigit() and len(identification_number) == 8:
            break
        else:
            print("Enter a valid Kenyan identification number. please ensure that you are an adult and an ID holder!")

# connecting to the db, sqlite3
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
        # closing the db connection
        conn.close()



                #   LOGIN METHOD
# creating the functionality of login in which handles the functionality of login in.
def login():
    username = input("Enter username to continue: ")
    password = getpass("Enter password to continue: ")
    identification_number = input("Enter your identification number: ")

# connecting to the server
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=? AND identification_number=?", 
                   (username, password, identification_number))
    user = cursor.fetchone()

# closing the server connection.

    conn.close()

# loop to ensure that the login is successful.
    if user:
        print("Login successful!")
        return user[0]
    else:
        print("Invalid username, password, or identification number! also try checking your spelling")
        return None

def admin_login():
    code = input("Enter admin code: ")

    if code == ADMIN_CODE:
        print("Admin login successful!")
        return True
    else:
        print("LOCKED!")
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


def view_votes_graphically():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    SELECT candidates.first_name, candidates.last_name, COUNT(votes.id) as vote_count
    FROM candidates
    LEFT JOIN votes ON candidates.id = votes.candidate_id
    GROUP BY candidates.id, candidates.first_name, candidates.last_name
    ''')
    results = cursor.fetchall()
    conn.close()

    if results:
        names = [f"{result[0]} {result[1]}" for result in results]
        vote_counts = [result[2] for result in results]

        plt.figure(figsize=(10, 5))
        plt.bar(names, vote_counts, color='skyblue')
        plt.xlabel('Candidates')
        plt.ylabel('Number of Votes')
        plt.title('Votes per Candidate')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
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

def delete_endorsement(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the user has endorsed a candidate
    cursor.execute("SELECT id FROM endorsements WHERE user_id=?", (user_id,))
    endorsement = cursor.fetchone()

    if endorsement:
        cursor.execute("DELETE FROM endorsements WHERE user_id=?", (user_id,))
        conn.commit()
        print("Endorsement deleted successfully!")
    else:
        print("You have not endorsed any candidate.")
    
    conn.close()




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


def main():
    initialize_db()
    update_db_schema()
    user_id = None
    admin_logged_in = False
    print("Welcome to Votemind, the future of a democratic engagement!"
          " At Votemind, we believe in the power of every voice and the"
          " importance of every vote. we are here to make your voting "
          "experience as seamless and straightforward as possible!"
          "You no longer have to make long ques under the scorching sun in "
          "order to vote for your preferred candidate!"
          "With our user_friendly interface, you can easily register, endorse "
          "candidates, and cast your vote with just"
          "just a few clicks. But that is not all! you can also view all the candidates,"
          " learn about their platforms, and see"
          "who is leading in endorsements. Our goal is to provide you with"
          " all the information that you need, and elect an informed leader. "
          "therefore, let's get started! Together, we can shape the future."
          " Remember, your vote counts!💪")
    
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
            print("\n1. Add Candidate\n2. View Candidate History\n3. Logout\n4. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                add_candidate()
            elif choice == '2':
                view_candidate_history()
            elif choice == '3':
                admin_logged_in = False
                print("Logged out successfully!")
                user_id = None
                break
            elif choice == '4':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            print("\n1. View Candidates\n2. View Votes\n3. View Endorsements\n4. View Votes Graphically\n5. Vote\n6. Endorse\n7. Delete Endorsement\n8. Logout\n9. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                view_candidates()
            elif choice == '2':
                view_votes()
            elif choice == '3':
                view_endorsements()
            elif choice == '4':
                view_votes_graphically()
            elif choice == '5':
                vote(user_id)
            elif choice == '6':
                endorse(user_id)
            elif choice == '7':
                delete_endorsement(user_id)
            elif choice == '8':
                user_id = None
                print("Logged out successfully!")
                break
            elif choice == '9':
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

                

if __name__ == "__main__":
    main()
