from predefinedhabits import predifined
import analytics
import datetime
import sys
from random import randint
import re


class Habits:
    def __init__(self, users_class):
          self.predefined_habits = predifined
          self.users_class = users_class
          self.database = self.users_class.db
          self.cursor = self.users_class.cursor


     
    def addPredefinedHabits(self):
        """
        Adds 5 predefined habits to db, predefined habits are from predefinedhabits.py 

        """

        # Retreiving predefined habits from predefined list file and adding them to the database

        self.users_class.return_id()
        add_predefined_habits = ( 
                '''insert into habits (user_id, habit_description, periodicity, date_added, due_date) 
                values(%s,%s,%s,%s,%s)'''
                ) 
        try:
            for habit in self.predefined_habits:
                    predifinedvalues = (self.users_class.user_id,) + tuple(habit)
                    self.cursor.execute(add_predefined_habits, predifinedvalues)
                    self.database.commit()
            
            print("Below you will find 5 predifined habits:")
            for habit in predifined:
                print(f" \n Habit: {habit[0]} \n Periodicity: {habit[1]}, \n Due date: {habit[3]} \n")  # Displays the predefined habits
        
        except:
             print("Error adding predefined habits")
    
    
    def main_menu(self):
        """
        Displays the main menu options for the user to input.
        """
        self.renew_habits()
        while True:
            menu_choose = input(
                ''' 
                [1] - Add Habit \n
                [2] - Check off Habit \n
                [3] - Delete habit \n
                [4] - Show all habits and relevant information \n
                [5] - Generate habit reports \n
                [6] - Quit \n
                '''
            ).strip()
                
            if menu_choose == "1":
                self.add_habit()
                break

            elif menu_choose == "2":
                self.check_off()
                break

            elif menu_choose == "3":
                self.delete_habit()
                break

            elif menu_choose == "4":
                self.show_all__relevant_habit_information()
                break

            elif menu_choose == "5":
                self.analytics_menu()
                break

            elif menu_choose == "6":
                sys.exit()
               
           
            else:
                print("invalid number")

    def add_habit(self):
        """
        Adds a new habit for a user to the database,

        Asks the user to specify a description and a periodicity

        """
      
        habit_date_added = datetime.date.today() 
        habit_due_date = datetime.date.today() 
        
        print("\n Here you can add habits by specifying the description and the periodicity (Either daily or weekly) \n")
        while True:
            habit_description = input("Please Enter the Habit description \n").strip()
            selection_query = ("Select habit_description from habits where user_id = %s and habit_description = %s")
            self.cursor.execute(selection_query,(self.users_class.user_id, habit_description,) )
            result = self.cursor.fetchone()
            
            # Validation

            if result:
                 print("Habit already exists")

            elif habit_description.isdigit():
                print("Habit cannot contain only numbers")

            elif len(habit_description) > 30 or len(habit_description) <=3:
                print("Habit description should be 3-30 characters long")

            elif not re.match(r"^(?!^[^a-zA-Z0-9]+$).*$", habit_description): 
                print("Habit description cannot contain only special characters")
            
            # Validation end
 
            else: 
                
                habit_periodicity = input("Please enter the habit periodicity: \n [1]- Daily \n [2]- Weekly \n  [3]- cancel \n ").strip()

                if habit_periodicity == "1" :
                    habit_due_date = datetime.datetime.combine(datetime.datetime.today() + datetime.timedelta(days=1), datetime.time())
                    break

                elif habit_periodicity == "2":
                    habit_due_date = datetime.datetime.combine(datetime.datetime.today() + datetime.timedelta(days=7), datetime.time())
                    break

                elif habit_periodicity == "3":
                    self.main_menu()

                else:
                    print("Please choose a valid option")

        # Habit insertion query

        add_habits_query = ("insert into habits (user_id, habit_description, periodicity, date_added, due_date) values(%s,%s,%s,%s,%s)")
        values = (self.users_class.user_id, habit_description, habit_periodicity, habit_date_added, habit_due_date)
        self.cursor.execute(add_habits_query, values)
        self.database.commit()
        print(f"Habit added successfully: due date: {habit_due_date}")

        self.after_action()
        
    
    def check_off(self):
        """
        Allows the user to specify a habit to check off, marks the habit as completed in the database.

        Increments/resets the streak upon renewal

        """
        check_off_date = datetime.datetime.today()

        fetch_habits_query = ("select habit_description from habits where user_id = %s and completed = %s ")
        self.cursor.execute(fetch_habits_query, (self.users_class.user_id, False,))
        habits = self.cursor.fetchall()

        if habits:

            print("""\n Here you can check off existing habits, each consecutive check off adds 1 to your habit streak when the habits are renewed, your habits are renewed automatically upon the expiry of the due date 
            \n Your current habits are: \n""")

            for habit in habits:
                print(f"- {habit[0]}")
        else:
            print("You currently have no habits.")
            self.main_menu()
        
        while True:
            check_off_description = input("Please enter the habit to be checked off \n input 1 to cancel \n").strip()
            
            if check_off_description == "1":
                self.main_menu()
                return
            
            # Habit check off queries
            
            else:
                selection_query = ("Select habit_description, completed, streak, longest_streak from habits where user_id = %s and habit_description = %s")
                self.cursor.execute(selection_query,(self.users_class.user_id, check_off_description,) )
                result = self.cursor.fetchall()

                for habit in result:

                    completed = habit[1]
                    streak = habit[2]
                    longest_streak = habit[3]
                
                if result and completed == False: 
                    streak+=1

                    if streak > longest_streak:
                        longest_streak = streak
            

                    completed_query = (
                        ''' 
                        update habits set completed = True, last_completed = %s, streak = %s , longest_streak = %s where habit_description = %s and user_id = %s
                        '''
                            )
                    
                    self.cursor.execute(completed_query, (check_off_date,streak, longest_streak,check_off_description, self.users_class.user_id))
                    self.database.commit()
                    print(f"Habit '{check_off_description}' was marked as complete")
                    break
                
                else:
                    print("Habit does not exist or is already complete")
            
        self.after_action()

   
    def delete_habit(self):
        """
        Allows the user to specify a habit to be deleted, habit and tracking record is deleted from the database.
        """
        fetch_habits_query = ("select habit_id, habit_description from habits where user_id = %s")
        self.cursor.execute(fetch_habits_query, (self.users_class.user_id,))
        habits = self.cursor.fetchall()

        if habits:
            print("""\n Here you can delete active or checked off habits, habit deletion is irreversable so please make sure you are 
 deleting the right habit \n \n Your current habits are:""")
            
            for habit in habits:
                print(f"- {habit[1]}")
        else:
            print("You currently have no habits.")
            self.main_menu()
        
         
        while True:
              deleted_habit = input("Please enter the habit you want to delete \n input 1 to cancel \n").strip()
              query = ("Select habit_id, habit_description from habits where user_id = %s and habit_description = %s")
              
               
              if deleted_habit == "1":
                self.main_menu()
                return
              
              else:

                # Selection query 
                self.cursor.execute(query,(self.users_class.user_id, deleted_habit,) )
                result = self.cursor.fetchone()
                
                if result:
                    habit_id = result[0]
                    delete_tracking_query = ("delete from habit_tracking where habit_id = %s")
                    self.cursor.execute(delete_tracking_query, (habit_id,)),
                    

                    query = ("delete from habits where user_id = %s and habit_description = %s")
                    self.cursor.execute(query, (self.users_class.user_id, deleted_habit))
                    self.database.commit()

                    print(f"Habit '{deleted_habit}' was deleted successfully")

                    break
                
                else:
                    print("Habit does not exist")
              
        self.after_action()

                   
    def after_action(self):
         """
         Function that allows the user to quit or go back to the main menu when an action is performed.
         """
         while True:
            
            after_adding = input("[1]- Main menu, [2]- Quit \n").strip()

            if after_adding == "1":
                 self.main_menu()
                 break
            
            elif after_adding == "2":
                 sys.exit()
            
            else:
                 print("Input valid option")

    
    def show_all__relevant_habit_information(self):
        """
        Shows the user all relevant information about their complete and incomplete habits.
        """
        query = ("Select habit_description, periodicity, due_date, completed from habits where user_id = %s ")
        self.cursor.execute(query, (self.users_class.user_id,))
        habits = self.cursor.fetchall()

        if habits:
            print("\n Your habits are: \n")
            for habit in habits:
                habit_description = habit[0]
                periodicity = habit[1]
                due_date = habit[2]
                completed = habit[3]

                completed_text = "" 
                
                if completed == False: 
                    completed_text = "Not complete"
                
                elif completed == True:
                    completed_text = "Complete"

                print(f"""
                Habit: {habit_description}\n
                Periodicity: {periodicity} \n
                Due date: {due_date} \n
                Habit {habit_description} is {completed_text}
                """
                )
            self.after_action()
        
        else:
            print("You have no habits")
            self.main_menu()
        
    
    def analytics_after_action(self):
        
        while True:
            after_action = input("""
            [1] - Main menu \n
            [2] - Generate more reports \n
            [3] - Quit
            """).strip()

            if after_action == "1":
                self.main_menu()
                break

            elif after_action == "2":
                self.analytics_menu()
                break
            
            elif after_action == "3":
                sys.exit()
            
            else:
                print("Input valid option")
            

    def renew_habits(self):
        """
        Renews habits upon expiry (when the due date is passed), assigns a new due date and increments/resets the habit streak.
        """
        query = ("select habit_id, periodicity, due_date, completed, streak, longest_streak, last_completed from habits where user_id = %s")
        self.cursor.execute(query, (self.users_class.user_id,))
        habits = self.cursor.fetchall()

        for habit in habits:
            habit_id = habit[0]
            periodicity = habit[1]
            due_date = datetime.datetime.combine(habit[2], datetime.time())
            completed = habit[3]
            habit_streak = habit[4]
            longest_streak = habit[5]
            last_completed = habit[6]

            if last_completed is not None:
                last_completed = datetime.datetime.combine(last_completed, datetime.time())
            else:
                 last_completed = due_date  # You can also use another suitable de

            new_due_date = due_date
    
            # Check if due date is expired to start renewing
            today = datetime.datetime.combine(datetime.date.today(), datetime.time())
            if due_date <= today:
                self.insert_expired_habit(habit_id, due_date, completed)

                # Exact Due time is set to midnight
                if periodicity == "Daily":
                    days_passed = (today.date() - last_completed.date()).days
                    new_due_date = datetime.datetime.combine(today + datetime.timedelta(days=1), datetime.time())

                    if days_passed >= 1 and completed == False:  # More than one day has passed and the habit was not completed
                        habit_streak = 0


                elif periodicity == "Weekly":
                    weeks_passed = (today.date() - last_completed.date()).days // 7
                    day_of_week_due = due_date.weekday()  # Day of week when the task is due. 0 for Monday, 1 for Tuesday, ..., 6 for Sunday.
                    days_till_next_due = (day_of_week_due - today.weekday() + 7) % 7
                    new_due_date = datetime.datetime.combine(today + datetime.timedelta(days=days_till_next_due), datetime.time())
                    
                    # If today is the due day, the task will be due next week.
                    if days_till_next_due == 0:
                        new_due_date += datetime.timedelta(days=7)

                    if weeks_passed > 0 and completed == False:  # More than one week has passed and the habit was not completed
                        habit_streak = 0          

                # Renew query
                renew = ("UPDATE habits SET due_date = %s, completed = %s, streak = %s, longest_streak = %s WHERE habit_id = %s")
                self.cursor.execute(renew, (new_due_date, False, habit_streak, longest_streak, habit_id,))
                self.database.commit()
                

    def insert_expired_habit(self, habit_id, due_date, completed):
        """
        Inserts expired habits into habit tracking table.
        """
        insert_query = "insert into habit_tracking (habit_id, due_date, completed) values (%s, %s, %s)"
        self.cursor.execute(insert_query, (habit_id, due_date, completed))
        self.database.commit() 

     

    def analytics_menu(self):
        """
        Displays the analytics menu for the user to generate reports regarding their habits
        """
        query = ("Select habit_description, periodicity, due_date, completed from habits where user_id = %s ")
        self.cursor.execute(query, (self.users_class.user_id,))
        habits = self.cursor.fetchall()
        if habits:
            print("\n Here you can analyze and show specific information about your habits \n")
            while True:
                analytics_choice = input(
                    """
                    [1] - Show list of incomplete habits \n
                    [2] - Show list of complete habits \n
                    [3] - Show all habits with a daily periodicity \n
                    [4] - Show all habits with a weekly periodicity \n
                    [5] - Show habit with the longest active streak \n
                    [6] - Show longest streak ever for a given habit \n
                    [7] - Back \n
                    [8] - Quit

                    """
                ).strip()

                if analytics_choice == '1':

                    incompleted = analytics.incomplete(self)  
                    
                    for incomplete in incompleted:
                        print(incomplete)

                    self.analytics_after_action()
                    break
            

                elif analytics_choice == '2':
                    completed = analytics.completed(self)

                    for complete in completed:
                        print(complete)

                    self.analytics_after_action()
                    break

                elif analytics_choice == '3':
                    daily_habits = analytics.habits_by_daily_periodicity(self)

                    for daily in daily_habits:
                        print(daily)   
                    self.analytics_after_action()
                    break
                    
                elif analytics_choice == '4':
                    weekly_habits = analytics.habits_by_weekly_periodicity(self)

                    for weekly in weekly_habits:
                        print(weekly)
                    self.analytics_after_action()
                    break
                    
                elif analytics_choice == '5':
                    
                    longest_streak_habit = analytics.longest_streak(self)
                    
                    for longest in longest_streak_habit:
                        print(longest)
                    self.analytics_after_action()
                    break
                    
                elif analytics_choice == '6':

                    # Display habits for user to input a specific habit
                    fetch_habits_query = ("select habit_id, habit_description from habits where user_id = %s")
                    self.cursor.execute(fetch_habits_query, (self.users_class.user_id,))
                    habits = self.cursor.fetchall()

                    if habits:
                        print("Your current habits are:")
                        for habit in habits:
                            print(f"- {habit[1]}")

                    # Input and output
      
                    habit_description = input("Enter the name of the habit: \n input 1 to cancel \n").strip()

                    if habit_description  == "1":
                        self.analytics_menu()
                        break

                    else:
                        longest_ever = analytics.longest_streak_ever(self, habit_description)

                        print(longest_ever)
                        self.analytics_after_action()
                        break
                
                elif analytics_choice == '7':
                    self.main_menu()
                    break

                elif analytics_choice == '8':
                    sys.exit()
                    
        else:
            print("You have no habits to analyze")
            self.main_menu()
            
         