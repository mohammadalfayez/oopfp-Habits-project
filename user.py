import mysql.connector
import re
import datetime
import analytics

class Database:
    """

    For establishing and closing a connection to the Database

    Args:
        host(str): Host database server location
        user(str): Username for db connection
        password(str): Password to connect to database
        database(str): Database name
        
    """
    
    def __init__(self, host="", user="", password="", database=""):
        """
        Enter your own database connection information and import the database I sent to load the database and test the code
        """
        try:
            self.db = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.db.cursor()
        except:
             print("Database connection failed")

    def close(self):
        """Closes the database"""
        self.cursor.close()
        self.db.close()
     

class Users:
    """

    Used for user authentication.

    Args:
        db(Database): instance of the database class to access instance attributes

    """
    def __init__(self,db):
        self.db = db.db
        self.cursor = self.db.cursor() 

        self.user_id = None
        self.username = ""
        self.password = ""
        
    def sign_up(self): 

        """
        Function for signing up, valid input is stored in db, db auto increments unique user ID

        """

        # username creation and validation
        while True: 
            self.username = input("Enter desired username (6-25 characters): \n").strip()

            query = ("Select username from users where username = %s")
            self.cursor.execute(query,(self.username,) )
            result = self.cursor.fetchone()
        
            if result:
                print("Username already exists")

            elif len(self.username) > 25 or len(self.username) <6:
                 print("Username must be 6-25 characters long")
            
            else:    
                break

        # End username creation and validation

        pass_condition = r"^(?=.*[!@#$%^&*()\-_=+{};:,<.>])^(?=.*\d).+$" # Regex for pw validation

        # Password creation and validation
        while True: 
            self.password = input("Enter desired password (must be atleast 8 characters long) \n").strip()
            if len(self.password) < 8:
                  print("Password must be atlest 8 characters long")

            elif not re.match(pass_condition,self.password):
                 print("Password must contain atleast 1 number and 1 special character")
                                            
            elif self.password == self.username :
                 print("Password cannot be the same as the username")

            else: 
                   
                insertion = ("Insert into users(username, user_password) values(%s, %s)")
                values = (self.username, self.password)
                self.cursor.execute(insertion,values)
                self.db.commit()
                print("Sign up successful \n") 
                break
                      
        # End password creation and validation

    
    def login(self): 
        """
        Function for logging in, input is retreived from db and validated
        """
        while True:
            self.username = input("Enter username \n").strip()
            self.password = input("Enter password \n").strip()
            
        
            query = ("Select username from users where username = %s and user_password = %s ")
            self.cursor.execute(query, (self.username, self.password, ))
            result = self.cursor.fetchone()
            
            if result:
                      print(f"Welcome {self.username}")
                      self.return_id()
                      print(self.user_id)
                      break
      
            else:
                print("Invalid username or password")
                

    def return_id(self):
                """
                Function that assigns the user id to the self.user_id attribute, will be used for the Habits class for user specific
                habits.

                Returns: 
                    int: the User ID
                """
                user_id_query = ("Select user_id from users where username = %s and user_password = %s ")
                self.cursor.execute(user_id_query, (self.username, self.password, ))
                result = self.cursor.fetchone()
                self.user_id = result[0]
            
                return self.user_id # User id will be used in almost every selection query



         


