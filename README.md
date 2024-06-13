# Votemind: Your Modern Voting Companion

Welcome to **Votemind**, a cutting-edge platform designed to revolutionize the democratic engagement process. Votemind empowers users to participate in elections seamlessly, endorsing candidates, casting votes, and staying informed—all from the convenience of their devices.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Contributing](#contributing)
- [License](#license)

## Features

### User Features
- **Registration and Login:** Securely register and log in using a username, password, and identification number.
- **View Candidates:** Browse through the list of registered candidates along with their details and images.
- **Vote:** Cast your vote for your preferred candidate.
- **Endorse Candidates:** Provide endorsements for candidates with a short summary.
- **View Votes:** See the vote counts for each candidate.
- **View Votes Graphically:** Visual representation of vote counts using bar charts.
- **Delete Endorsements:** Remove your previous endorsements if necessary.

### Admin Features
- **Admin Login:** Secure admin login using a special admin code.
- **Add Candidates:** Add new candidates with detailed information.
- **Update Candidates:** Modify existing candidate details.
- **Delete Candidates:** Remove candidates from the list.
- **View Registered Candidates:** See the total number of registered candidates.
- **View Users Voted:** Check the number of users who have cast their votes.
- **View Candidate History:** Access the detailed history of each candidate.

## Installation

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- SQLite3
- `pip` package manager

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/votemind.git
   cd votemind
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**

   The database will be automatically initialized when you run the application for the first time.

## Usage

1. **Run the CLI application:**

   ```bash
   python cli.py
   ```

2. **Follow the on-screen instructions to register, log in, and use the application.**

### User Operations

- **Register:** Enter your username,

password, and an 8-digit identification number.
- **Login:** Use your credentials to access your account.
- **View Candidates:** Browse through the list of candidates to learn about their platforms.
- **Vote:** Select and vote for your preferred candidate.
- **Endorse Candidates:** Provide a short summary to endorse a candidate.
- **View Votes:** Check the current vote counts for each candidate.
- **View Votes Graphically:** Visualize the vote counts using bar charts.
- **Delete Endorsements:** Remove your previous endorsements if needed.

### Admin Operations

- **Admin Login:** Use the special admin code to access admin features.
- **Add Candidates:** Enter candidate details to add them to the list.
- **Update Candidates:** Modify existing candidate details as necessary.
- **Delete Candidates:** Remove candidates from the list.
- **View Registered Candidates:** See the total number of candidates who have registered.
- **View Users Voted:** Check the number of users who have cast their votes.
- **View Candidate History:** Access and review detailed histories of each candidate.

## Project Structure

The project is organized into several modules, each responsible for different functionalities:

```plaintext
votemind/
├── db/
│   └── votemind.db  # SQLite database file
├── cli.py           # Main CLI application
├── db_init.py       # Database initialization and schema update
├── auth_functions.py# User and Admin authentication
├── user_functions.py# User functionalities (view candidates, vote, endorse, etc.)
├── admin_functions.py# Admin functionalities (add, update, delete candidates, etc.)
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

## Database Schema

The database schema includes the following tables:

- **Users:** Stores user credentials and identification numbers.
- **Candidates:** Stores candidate details including their platform and history.
- **Votes:** Tracks the votes cast by users.
- **Endorsements:** Tracks endorsements made by users for candidates.

### Table Definitions

- **Users:**

  ```sql
  CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE,
      password TEXT,
      identification_number TEXT UNIQUE
  );
  ```

- **Candidates:**

  ```sql
  CREATE TABLE IF NOT EXISTS candidates (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      first_name TEXT,
      last_name TEXT,
      party TEXT,
      description TEXT,
      image_url TEXT,
      history TEXT
  );
  ```

- **Votes:**

  ```sql
  CREATE TABLE IF NOT EXISTS votes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      candidate_id INTEGER,
      FOREIGN KEY(user_id) REFERENCES users(id),
      FOREIGN KEY(candidate_id) REFERENCES candidates(id)
  );
  ```

- **Endorsements:**

  ```sql
  CREATE TABLE IF NOT EXISTS endorsements (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER,
      candidate_id INTEGER,
      summary TEXT,
      FOREIGN KEY(user_id) REFERENCES users(id),
      FOREIGN KEY(candidate_id) REFERENCES candidates(id)
  );
  ```

## Contributing

We welcome contributions to enhance Votemind. If you are interested in contributing, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Open a pull request to the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Thank you for choosing Votemind. Together, we can make every vote count and shape a better future. For any queries or support, please contact us at [support@votemind.com](mailto:support@votemind.com).