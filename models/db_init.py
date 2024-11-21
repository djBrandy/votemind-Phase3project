import os
# Importing sqlite3 module for database operations
import sqlite3


# getting the directory of the current script:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Setting the path of the database
DB_PATH = os.path.join(BASE_DIR, '..', 'db', 'votemind.db')

# Function to initialize the database
def initialize_db():
    # Connecting to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Creating tables if they do not exist
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        identification_number TEXT UNIQUE
    )
    ''')

    # Candidates table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        party TEXT,
        description TEXT,
        image_url TEXT,
        history TEXT
    )
    ''')

    # Votes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        candidate_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(candidate_id) REFERENCES candidates(id)
    )
    ''')

    # Endorsements table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS endorsements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        candidate_id INTEGER,
        summary TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(candidate_id) REFERENCES candidates(id)
    )
    ''')

    # Candidate endorsements table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidate_endorsements (
        candidate_id INTEGER,
        endorsement_id INTEGER,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id),
        FOREIGN KEY(endorsement_id) REFERENCES endorsements(id),
        PRIMARY KEY (candidate_id, endorsement_id)
    )
    ''')

    # Committing the changes and closing the connection
    conn.commit()
    conn.close()

# Function to update the database schema
def update_db_schema():
    # Connecting to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Adding new columns to the endorsements and candidates tables if they do not exist
    try:
        cursor.execute('ALTER TABLE endorsements ADD COLUMN summary TEXT')
    except sqlite3.OperationalError:
        pass  # The column already exists
    
    try:
        cursor.execute('ALTER TABLE candidates ADD COLUMN history TEXT')
    except sqlite3.OperationalError:
        pass  # The column already exists

    # Creating the candidate_endorsements table if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidate_endorsements (
        candidate_id INTEGER,
        endorsement_id INTEGER,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id),
        FOREIGN KEY(endorsement_id) REFERENCES endorsements(id),
        PRIMARY KEY (candidate_id, endorsement_id)
    )
    ''')

    # Committing the changes and closing the connection
    conn.commit()
    conn.close()