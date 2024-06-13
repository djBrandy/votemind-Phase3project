# Importing necessary functions from other files
from db_init import initialize_db, update_db_schema
from auth_functions import User, Admin
from user_functions import UserFunctions
from admin_functions import AdminFunctions

# CLI class to handle the command line interface for the application
class CLI:
    def __init__(self):
        # Initializing user and admin objects along with their respective function objects
        self.user = User()
        self.admin = Admin()
        self.user_functions = UserFunctions()
        self.admin_functions = AdminFunctions()
        # Initializing user_id and admin_logged_in variables
        self.user_id = None
        self.admin_logged_in = False

    def main(self):
        # Initialize and update the database
        initialize_db()
        update_db_schema()

        # Welcome message
        print("Welcome to Votemind, the future of democratic engagement!\n"
              "...")

        # Loop until a user or admin logs in
        while self.user_id is None and not self.admin_logged_in:
            print("\n1. Register\n2. Login\n3. Admin Login\n4. Exit")
            choice = input("Enter your choice: ")

            # Handle user's choice
            if choice == '1':
                self.user.register()
            elif choice == '2':
                self.user_id = self.user.login()
            elif choice == '3':
                self.admin_logged_in = self.admin.admin_login()
            elif choice == '4':
                print("Goodbye!")
                return
            else:
                print("Invalid choice. Please try again.")

        # Main loop for handling user or admin actions
        while True:
            if self.admin_logged_in:
                print("\nAdmin Menu:\n1. Add Candidate\n2. Update Candidate\n3. Delete Candidate\n"
                      "4. View Candidate History\n5. View Registered Candidates\n6. View Users Voted\n"
                      "7. Logout\n8. Exit")
                choice = input("Enter your choice: ")

                # Handle admin's choice
                if choice == '1':
                    self.admin_functions.add_candidate()
                elif choice == '2':
                    self.admin_functions.update_candidate()
                elif choice == '3':
                    self.admin_functions.delete_candidate()
                elif choice == '4':
                    self.admin_functions.view_candidate_history()
                elif choice == '5':
                    self.admin_functions.view_registered_candidates()
                elif choice == '6':
                    self.admin_functions.view_users_voted()
                elif choice == '7':
                    self.admin_logged_in = False
                    print("Logged out successfully!")
                    self.user_id = None
                    break
                elif choice == '8':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            else:
                print("\nUser Menu:\n1. View Candidates\n2. View Votes\n3. View Votes Graphically\n4. View Endorsements\n"
                      "5. Vote\n6. Endorse\n7. Delete Endorsement\n8. Logout\n9. Exit")
                choice = input("Enter your choice: ")

                # Handle user's choice
                if choice == '1':
                    self.user_functions.view_candidates()
                elif choice == '2':
                    self.user_functions.view_votes()
                elif choice == '3':
                    self.user_functions.view_votes_graphically()
                elif choice == '4':
                    self.user_functions.view_endorsements()
                elif choice == '5':
                    self.user_functions.vote(self.user_id)
                elif choice == '6':
                    self.user_functions.endorse(self.user_id)
                elif choice == '7':
                    self.user_functions.delete_endorsement(self.user_id)
                elif choice == '8':
                    print("Logged out successfully!")
                    self.user_id = None
                    break
                elif choice == '9':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")

# Main function to start the application
if __name__ == "__main__":
    cli = CLI()
    cli.main()
