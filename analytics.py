import mysql.connector


def incomplete(habits_class):
    
    completed = False
    """
    Filters and returns habits based on the completion status.
    """
    fetch_habits_query = (
        "select habit_description, due_date from habits where user_id = %s and completed = %s"
    )
    habits_class.cursor.execute(
        fetch_habits_query,
        (habits_class.users_class.user_id, completed,),
    )
    habits = habits_class.cursor.fetchall()


    if habits:
         return [f"{habit[0]}: {habit[1]} \n" for habit in habits]
     
    else:
        return ["No Incomplete habits"]


def completed (habits_class):
    
    completed = True
    """
    Filters and returns habits based on the completion status.
    """
    fetch_habits_query = (
        "select habit_description, periodicity from habits where user_id = %s and completed = %s"
    )
    habits_class.cursor.execute(
        fetch_habits_query,
        (habits_class.users_class.user_id, completed,),
    )
    habits = habits_class.cursor.fetchall()

    
    if habits:
         return [f"{habit[0]}: {habit[1]} \n" for habit in habits]
    else:
        return ["No completed habits"]



def habits_by_daily_periodicity(habits_class):
    """
    Retrieves habits based on the specified periodicity.

    Args:
        habits_class: An instance of the Habits class.
        periodicity: The periodicity value to filter habits.

    Returns:
        A list of habit descriptions with the specified periodicity.
    """
    fetch_habits_query = "select habit_description from habits where user_id = %s and periodicity = 'Daily' "
    habits_class.cursor.execute(fetch_habits_query, (habits_class.users_class.user_id, ))
    habits = habits_class.cursor.fetchall()

    if habits:
        return [f"{habit[0]}" for habit in habits]
    else:
        return ["No daily habits"]


def habits_by_weekly_periodicity(habits_class):
    """
    Retrieves habits based on the specified periodicity.

    Args:
        habits_class: An instance of the Habits class.
        periodicity: The periodicity value to filter habits.

    Returns:
        A list of habit descriptions with the specified periodicity.
    """
    fetch_habits_query = "select habit_description from habits where user_id = %s and periodicity = 'Weekly'"
    habits_class.cursor.execute(fetch_habits_query, (habits_class.users_class.user_id,))
    habits = habits_class.cursor.fetchall()
    
    if habits:
        return [f"{habit[0]}" for habit in habits]
    
    else:
        return ["No weekly habits"]

def longest_streak(habits_class):
    """
    Retrieves the habits with the highest streak.

    Args:
        habits_class: An instance of the Habits class.

    Returns:
        A list of strings, each representing a habit with the highest streak.
    """
    # fetch the highest streak
    fetch_highest_streak_query = """
        select max(streak) from habits where user_id = %s
    """
    habits_class.cursor.execute(fetch_highest_streak_query, (habits_class.users_class.user_id,))
    highest_streak = habits_class.cursor.fetchone()[0]
    
    if highest_streak == 0:
        return ["All habits have a streak of 0"]
    
    else:
        # fetch habits with the highest streak
        fetch_longest_streak_habits_query = """
            select habit_description, streak from habits 
            where user_id = %s and streak = %s
        """
        habits_class.cursor.execute(fetch_longest_streak_habits_query, (habits_class.users_class.user_id, highest_streak))
        longest_streak_habits = habits_class.cursor.fetchall()

        return [f"{habit[0]}: Streak: {habit[1]} \n" for habit in longest_streak_habits]



def longest_streak_ever(habits_class, habit_description):
    """
    Retrieves the longest streak ever for a given habit.

    Args:
        habits_class: An instance of the Habits class.
        habit_description: The description of the habit.

    Returns:
        The longest streak ever for the habit.
    """
    fetch_longest_streak_query = "select longest_streak from habits where user_id = %s and habit_description = %s"

    habits_class.cursor.execute(fetch_longest_streak_query, (habits_class.users_class.user_id, habit_description,))
    longest_streak = habits_class.cursor.fetchone()

    if longest_streak:
        return longest_streak[0]
    
    else:
        return f"No habit found with description '{habit_description}'"

