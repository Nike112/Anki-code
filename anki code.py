import tkinter as tk
import random
import mysql.connector

# Replace the following with your MySQL database details
db_config = {
    'host': 'localhost',
    'user': 'Niketh',
    'password': 'Root@123',
    'database': 'anki',
}

# Establish a connection to MySQL
db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()

# Create a table if it doesn't exist
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        player_name VARCHAR(255) NOT NULL,
        win_loss VARCHAR(10) NOT NULL,
        no_of_guesses INT NOT NULL
    )
''')
db_connection.commit()

root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("400x480")  # Fixed geometry

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (400 / 2)
y_coordinate = (screen_height / 2) - (400 / 2)
root.geometry("+%d+%d" % (x_coordinate, y_coordinate))

# Player Name Entry
player_name_label = tk.Label(root, text="Enter Your Name:")
player_name_label.grid(row=0, column=0, columnspan=4, pady=10, sticky='nsew')

player_name_entry = tk.Entry(root, bd=2, relief='solid')
player_name_entry.grid(row=1, column=0, columnspan=4, pady=10, sticky='nsew')

# Start/Reset Buttons
start_button = tk.Button(root, text="Start Game")
start_button.grid(row=2, column=0, columnspan=4, pady=10, sticky='nsew')

reset_button = tk.Button(root, text="Reset Game", state=tk.DISABLED)
reset_button.grid(row=3, column=0, columnspan=4, pady=10, sticky='nsew')

# Guess Entry
guess_label = tk.Label(root, text="Enter Your Guess:")
guess_label.grid(row=4, column=0, columnspan=4, pady=10, sticky='nsew')

guess_entry = tk.Entry(root, bd=2, relief='solid')
guess_entry.grid(row=5, column=0, columnspan=4, pady=10, sticky='nsew')

# Guess Button
guess_button = tk.Button(root, text="Submit Guess", state=tk.DISABLED)
guess_button.grid(row=6, column=0, columnspan=4, pady=10, sticky='nsew')

# Hint Box
hint_box = tk.Label(root, text="")
hint_box.grid(row=7, column=0, columnspan=4, pady=10, sticky='nsew')

# No of Guesses
guess_count_label = tk.Label(root, text="No of Guesses:")
guess_count_label.grid(row=8, column=0, columnspan=2, pady=10, sticky='nsew')

guess_count = tk.Label(root, text="0")
guess_count.grid(row=8, column=2, columnspan=2, pady=10, sticky='nsew')

# No of Guesses Left
guesses_left_label = tk.Label(root, text="Guesses Left:")
guesses_left_label.grid(row=9, column=0, columnspan=2, pady=10, sticky='nsew')

guesses_left = tk.Label(root, text="10")
guesses_left.grid(row=9, column=2, columnspan=2, pady=10, sticky='nsew')

# Exit Button
exit_button = tk.Button(root, text="Exit Game", command=root.destroy)
exit_button.grid(row=10, column=0, columnspan=4, pady=10, sticky='nsew')

target_number = 0
guesses = 0

player_name = ""

def start_game():
    global target_number, guesses, player_name
    player_name = player_name_entry.get()
    target_number = random.randint(1, 100)
    guesses = 0
    # print(target_number)

    start_button.config(state=tk.DISABLED)
    reset_button.config(state=tk.NORMAL)
    guess_button.config(state=tk.NORMAL)

def reset_game():
    global target_number, guesses
    target_number = 0
    guesses = 0

    player_name_entry.delete(0, tk.END)
    guess_entry.delete(0, tk.END)
    hint_box.config(text="")
    guess_count.config(text="0")
    guesses_left.config(text="10")

    start_button.config(state=tk.NORMAL)
    reset_button.config(state=tk.DISABLED)
    guess_button.config(state=tk.DISABLED)

def check_guess():
    global target_number, guesses
    guess = int(guess_entry.get())
    guess_entry.delete(0, tk.END)

    guesses += 1
    guess_count.config(text=str(guesses))
    guesses_left_value = 10 - guesses
    guesses_left.config(text=str(guesses_left_value))

    if guess == target_number:
        hint_box.config(text=f"Congratulations, {player_name}! You guessed the correct number.")
        save_result("Win", guesses)
        guess_button.config(state=tk.DISABLED)
    elif guess < target_number:
        hint_box.config(text="Go Higher!")
    else:
        hint_box.config(text="Go Lower!")

    if (guesses_left_value == 0) and (guess != target_number):
        hint_box.config(text=f"Sorry, {player_name}! You've run out of guesses. The correct number was {target_number}.")
        save_result("Loss", guesses)
        guess_button.config(state=tk.DISABLED)

def save_result(result, num_of_guesses):
    # Save the result to the database
    db_cursor.execute('''
        INSERT INTO results(player_name, win_loss, no_of_guesses)
        VALUES (%s, %s, %s)
    ''', (player_name, result, num_of_guesses))
    db_connection.commit()

# Set grid weights to make the center columns expandable
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

# Configure button commands
start_button.config(command=start_game)
reset_button.config(command=reset_game)
guess_button.config(command=check_guess)

# Run the Tkinter event loop
root.mainloop()

# Close the database connection when the program ends
db_cursor.close()
db_connection.close()
