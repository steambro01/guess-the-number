import random
import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        sql_create_table = """ CREATE TABLE IF NOT EXISTS scoreboard (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL,
                                    attempts INTEGER
                                ); """
        conn.cursor().execute(sql_create_table)
    except sqlite3.Error as e:
        print(e)

def save_result(conn, name, attempts):
    sql = ''' INSERT INTO scoreboard(name, attempts)
              VALUES(?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (name, attempts))
    conn.commit()

def display_scoreboard():
    conn = create_connection('scoreboard.db')
    if conn is not None:
        cur = conn.cursor()
        cur.execute("SELECT name, attempts FROM scoreboard ORDER BY attempts ASC LIMIT 10")
        rows = cur.fetchall()
        print("\nTop 10 Scores:")
        for row in rows:
            print(f"{row[0]}: {row[1]} attempts")
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

def guess_the_number():
    print("Welcome to the Guess the Number Game!")
    print("I have selected a number between 1 and 100. Try to guess it!")

    # Randomly select a number between 1 and 100
    number_to_guess = random.randint(1, 100)
    attempts = 0

    # Ask for the user's name
    name = input("Enter your name: ")

    while True:
        try:
            # Ask the user for their guess
            guess = int(input("Enter your guess: "))
            attempts += 1

            # Check if the guess is correct
            if guess < number_to_guess:
                print("Too low! Try again.")
            elif guess > number_to_guess:
                print("Too high! Try again.")
            else:
                print(f"Congratulations, {name}! You guessed the number in {attempts} attempts.")
                
                # Save the result to the database
                conn = create_connection('scoreboard.db')
                if conn is not None:
                    save_result(conn, name, attempts)
                    conn.close()
                else:
                    print("Error! Cannot create the database connection.")
                
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

# Run the game and display the scoreboard
if __name__ == "__main__":
    # Create the database and table if they don't exist
    conn = create_connection('scoreboard.db')
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

    guess_the_number()
    display_scoreboard()
