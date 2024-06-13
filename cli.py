from db_init import initialize_db, update_db_schema
from auth_functions import register, login, admin_login
from user_functions import (view_candidates, view_votes, view_votes_graphically, 
                            view_endorsements, vote, endorse, delete_endorsement)
from admin_functions import (add_candidate, update_candidate, delete_candidate, 
                             view_registered_candidates, view_users_voted, view_candidate_history)

def main():
    # Initialize and update the database
    initialize_db()
    update_db_schema()

    # Welcome message
    print("Welcome to Votemind, the future of democratic engagement!\n"
          "At Votemind, we believe in the power of every voice and the importance of every vote.\n"
          "We are here to make your voting experience as seamless and straightforward as possible!\n"
          "You no longer have to make long queues under the scorching sun in order to vote for your preferred candidate!\n"
          "With our user-friendly interface, you can easily register, endorse candidates, and cast your vote with just a few clicks.\n"
          "But that is not all! You can also view all the candidates, learn about their platforms, and see who is leading in endorsements.\n"
          "Our goal is to provide you with all the information that you need, and elect an informed leader.\n"
          "Therefore, let's get started! Together, we can shape the future. Remember, your vote counts! 💪")

    user_id = None
    admin_logged_in = False

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
            print("\nAdmin Menu:\n1. Add Candidate\n2. Update Candidate\n3. Delete Candidate\n"
                  "4. View Candidate History\n5. View Registered Candidates\n6. View Users Voted\n"
                  "7. Logout\n8. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                add_candidate()
            elif choice == '2':
                update_candidate()
            elif choice == '3':
                delete_candidate()
            elif choice == '4':
                view_candidate_history()
            elif choice == '5':
                view_registered_candidates()
            elif choice == '6':
                view_users_voted()
            elif choice == '7':
                admin_logged_in = False
                print("Logged out successfully!")
                user_id = None
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

            if choice == '1':
                view_candidates()
            elif choice == '2':
                view_votes()
            elif choice == '3':
                view_votes_graphically()
            elif choice == '4':
                view_endorsements()
            elif choice == '5':
                vote(user_id)
            elif choice == '6':
                endorse(user_id)
            elif choice == '7':
                delete_endorsement(user_id)
            elif choice == '8':
                print("Logged out successfully!")
                user_id = None
                break
            elif choice == '9':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
