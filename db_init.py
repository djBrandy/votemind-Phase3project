import sqlite3

DB_PATH = 'db/votemind.db'

def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        identification_number TEXT UNIQUE
    )
    ''')

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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        candidate_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(candidate_id) REFERENCES candidates(id)
    )
    ''')

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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidate_endorsements (
        candidate_id INTEGER,
        endorsement_id INTEGER,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id),
        FOREIGN KEY(endorsement_id) REFERENCES endorsements(id),
        PRIMARY KEY (candidate_id, endorsement_id)
    )
    ''')

    conn.commit()
    conn.close()

def update_db_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('ALTER TABLE endorsements ADD COLUMN summary TEXT')
    except sqlite3.OperationalError:
        pass  # The column already exists
    
    try:
        cursor.execute('ALTER TABLE candidates ADD COLUMN history TEXT')
    except sqlite3.OperationalError:
        pass  # The column already exists

    # Create candidate_endorsements table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidate_endorsements (
        candidate_id INTEGER,
        endorsement_id INTEGER,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id),
        FOREIGN KEY(endorsement_id) REFERENCES endorsements(id),
        PRIMARY KEY (candidate_id, endorsement_id)
    )
    ''')

    conn.commit()
    conn.close()
