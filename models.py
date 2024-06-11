# Importing the sqlite3 module to interact with a SQLite database
import sqlite3


# Function to initialize the database
def initialize_db():
    # Connecting to your SQLite database
    conn = sqlite3.connect('db/votemind.db')
     # Creating a cursor object to execute SQL commands
    cursor = conn.cursor()
    
    # Creating the users table if it does not already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        identification_number TEXT UNIQUE NOT NULL
    )
    ''')

    # Creating the candidates table if it does not already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        party TEXT NOT NULL
    )
    ''')
    
    # Creating the votes table if it does not already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        candidate_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (candidate_id) REFERENCES candidates(id)
    )
    ''')
    

    # Creating the endorsements table if it does not already exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS endorsements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        candidate_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (candidate_id) REFERENCES candidates(id)
    )
    ''')
    
    # Committing the changes to the database
    conn.commit()

    # Closing the connection to the database
    conn.close()

if __name__ == "__main__":
    # Running the initialize_db function when the script is run directly
    initialize_db()
