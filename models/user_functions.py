import os
# Importing sqlite3 module for database operations and matplotlib for data visualization
import sqlite3
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Setting the path of the database
DB_PATH = os.path.join(BASE_DIR, '..', 'db', 'votemind.db')

# UserFunctions class to handle the user related operations
class UserFunctions:
    # Function to view all candidates
    def view_candidates(self):
        # Connecting to the database and executing the SELECT query
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_name, last_name, party, description, image_url FROM candidates")
        candidates = cursor.fetchall()
        conn.close()

        # Printing the candidates if found
        if candidates:
            print("Candidates:")
            for candidate in candidates:
                print(f"{candidate[0]}. {candidate[1]} {candidate[2]} ({candidate[3]}) - {candidate[4]}")
                print(f"Image URL: {candidate[5]}\n")
        else:
            print("No candidates found.")

    # Function to view the vote counts for all candidates
    def view_votes(self):
        # Connecting to the database and executing the SELECT query
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

        # Printing the vote counts if found
        if results:
            print("Vote Counts:")
            for result in results:
                print(f"{result[0]}. {result[1]} {result[2]} ({result[3]}) - {result[4]} votes")
        else:
            print("No votes found.")

    # Function to view the vote counts graphically
    def view_votes_graphically(self):
        # Connecting to the database and executing the SELECT query
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

        # Plotting the vote counts if found
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

    # Function to view the endorsements for all candidates
    def view_endorsements(self):
        # Connecting to the database and executing the SELECT query
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

        # Printing the endorsement counts and summaries if found
        if results:
            print("Endorsement Counts and Summaries:")
            for result in results:
                print(f"{result[0]}. {result[1]} {result[2]} ({result[3]}) - {result[4]} endorsements")
                print(f"Endorsement Summaries:\n{result[5]}")
        else:
            print("No endorsements found.")

    # Function to vote for a candidate
    def vote(self, user_id):
        # Displaying the candidates for the user to choose from
        self.view_candidates()
        candidate_id = int(input("Enter the candidate ID to vote for: "))

        # Connecting to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Checking if the user has already voted
        cursor.execute("SELECT id FROM votes WHERE user_id=?", (user_id,))
        vote = cursor.fetchone()
        
        # If the user has already voted, print a message
        if vote:
            print("You have already voted!")
        else:
            # If the user has not voted, record the vote
            try:
                cursor.execute("INSERT INTO votes (user_id, candidate_id) VALUES (?, ?)", (user_id, candidate_id))
                conn.commit()
                print("Vote recorded successfully!")
            except sqlite3.IntegrityError:
                print("An error occurred while recording your vote.")
            finally:
                conn.close()

    # Function to endorse a candidate
    def endorse(self, user_id):
        # Displaying the candidates for the user to choose from
        self.view_candidates()
        candidate_id = int(input("Enter the candidate ID to endorse: "))
        summary = input("Enter a short summary for your endorsement: ")

        # Connecting to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Checking if the user has already endorsed a candidate
        cursor.execute("SELECT id FROM endorsements WHERE user_id=?", (user_id,))
        endorsement = cursor.fetchone()

        # If the user has already endorsed a candidate, print a message
        if endorsement:
            print("You have already endorsed a candidate!")
        else:
            # If the user has not endorsed a candidate, record the endorsement
            try:
                cursor.execute("INSERT INTO endorsements (user_id, candidate_id, summary) VALUES (?, ?, ?)", (user_id, candidate_id, summary))
                conn.commit()
                print("Endorsement recorded successfully!")
            except sqlite3.IntegrityError:
                print("An error occurred while recording your endorsement.")
            finally:
                conn.close()

    # Function to delete an endorsement
    def delete_endorsement(self, user_id):
        # Connecting to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Checking if the user has endorsed a candidate
        cursor.execute("SELECT id FROM endorsements WHERE user_id=?", (user_id,))
        endorsement = cursor.fetchone()

        # If the user has endorsed a candidate, delete the endorsement
        if endorsement:
            cursor.execute("DELETE FROM endorsements WHERE user_id=?", (user_id,))
            conn.commit()
            print("Endorsement deleted successfully!")
        else:
            print("You have not endorsed any candidate.")
        
        conn.close()