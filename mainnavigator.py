from user import Users
from user import Database
from habits import Habits
import sys
def main_navigator():
     """
     Function to control and execute the application navigation flow. 
     """
     db = Database()
     user = Users(db)
     habit = Habits(user)

     while True:
            choose_option = input("Welcome! \n Input [1] to sign up, \n Input [2] to log in \n, Input [3] to quit \n").strip()
        
            if choose_option == "1":
                user.sign_up()
                habit.addPredefinedHabits()

                while True:
                    after_signup_choose = input("[1] Main menu? \n [2] Quit \n").strip()
                    if after_signup_choose == "1":
                        habit.main_menu()
                        return

                    elif after_signup_choose == "2":
                        print("Quitting")
                        sys.exit()
                        
                    else:
                        print("Please pick a valid option")

            elif choose_option == "2":
                user.login()
                habit.main_menu()
                break
            
            elif choose_option == "3":
                 print("Quitting")
                 sys.exit()
            
            else:
                 print("input valid number")

     db.close()

    
main_navigator()
