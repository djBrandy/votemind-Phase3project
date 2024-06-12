import sqlite3
from getpass import getpass
import matplotlib.pyplot as plt
from db_init import DB_PATH

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

    cursor.execute("SELECT id FROM endorsements WHERE user_id=?", (user_id,))
    endorsement = cursor.fetchone()

    if endorsement:
        cursor.execute("DELETE FROM endorsements WHERE user_id=?", (user_id,))
        conn.commit()
        print("Endorsement deleted successfully!")
    else:
        print("You have not endorsed any candidate.")
    
    conn.close()
