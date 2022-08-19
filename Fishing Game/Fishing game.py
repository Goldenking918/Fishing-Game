# Imports different packages used.
from tkinter import *
import tkinter as tk
import random
from PIL import Image, ImageTk

# Creates the Window for the Starting Main Menu
root = Tk()
root.wait_visibility()
root.title("Fishing Game")
root.geometry("1280x720")
root.resizable(False, False)

# Creates the frames for the main frame and fishing frame.
main_frame = tk.Frame(root)
fishing_frame = tk.Frame(root)

# Creates variables to be used throughout the program.
x = 1
difficulty = ""
fish_type = 0
fish_size = 0
score = 0
countdown = 30
start = False
name = ""
sort_easy = []
sort_medium = []
sort_hard = []
top_easy = ""
top_medium = ""
top_hard = ""

# Defines images that are used in the program.
Salmon_image = ImageTk.PhotoImage(Image.open("images/Salmon.jpeg"))
Tuna_image = ImageTk.PhotoImage(Image.open("images/Tuna.png"))
Cod_image = ImageTk.PhotoImage(Image.open("images/Cod.jpeg"))
Mackerel_image = ImageTk.PhotoImage(Image.open("images/Mackerel.jpeg"))

# -----------------------------Functions------------------------------


# Changes the main menu into the fishing game.
def button_game():
    global top_easy, top_medium, top_hard
    top_easy = ""
    top_medium = ""
    top_hard = ""

    fishing_frame.pack(fill="both", expand=1)
    change_size()
    main_frame.forget()


# Returns to the main menu frame.
def return_menu():
    global x, score, start
    # Resets some of the variables
    x = 1
    score = 0
    start = False
    game_score.config(text=f"Score:{score}")
    reset_countdown()
    main_frame.pack(fill="both", expand=1)
    fishing_frame.forget()
    display_scores()


# Randomly determines the type of fish and its size using a nested list.
def change_size():
    global fish_type, fish_size
    fish_type = random.randint(0, 3)
    fish_size = random.randint(0, 3)
    text_game.config(text=Fish_list[fish_type][fish_size])
    if fish_type == 0:
        image_game.config(image=Salmon_image)
    elif fish_type == 1:
        image_game.config(image=Tuna_image)
    elif fish_type == 2:
        image_game.config(image=Cod_image)
    elif fish_type == 3:
        image_game.config(image=Mackerel_image)


# Changes variables for the different difficulty in the game
def easy():
    global x, difficulty, start, score
    difficulty = "easy"
    start = True
    score = 0
    button_game()
    start_countdown()


def medium():
    global x, difficulty, start, score, countdown
    difficulty = "medium"
    start = True
    score = 0
    countdown = 35
    button_game()
    start_countdown()


def hard():
    global x, difficulty, start, score, countdown
    difficulty = "hard"
    start = True
    score = 0
    countdown = 40
    button_game()
    start_countdown()


# Changes the amount of images displayed in each difficulty.
def end_check():
    global difficulty
    if difficulty == "easy":
        if x == 11:
            show_results()
    elif difficulty == "medium":
        if x == 16:
            show_results()
    elif difficulty == "hard":
        if x == 21:
            show_results()


# Changes the image every time the buttons are clicked.
def catch():
    global x
    x += 1
    catch_check()
    end_check()
    change_size()


def release():
    global x
    x += 1
    release_check()
    end_check()
    change_size()


# Increases the score if the fish size is right.
def catch_check():
    global score
    if fish_size == 0 or fish_size == 2:
        score += 1
        game_score.config(text=f"Score:{score}")


def release_check():
    global score
    if fish_size == 1 or fish_size == 3:
        score += 1
        game_score.config(text=f"Score:{score}")


# Starts the countdown
def start_countdown():
    global countdown
    if start:
        # Lowers the countdown by one every second
        countdown -= 10
        game_countdown.configure(text=f"Time:{countdown}")
        root.after(1000, start_countdown)
        if countdown == 0:
            show_results()

    else:
        pass

    return countdown


# Resets and stops the countdown
def reset_countdown():
    global countdown, start
    start = False
    countdown = 30
    game_countdown.configure(text=f"Time:{countdown}")


# Creates a new window displaying score after the game is finished.
def show_results():
    global countdown, score, start
    start = False
    # Creates the new window.
    result = Toplevel(root)
    result.update()
    result.geometry("700x400")
    result.resizable(False, False)
    result.title("Level Finished")
    result.grab_set()
    result.config(bg="light blue")
    result_text = Label(result, font=("Trebuchet MS", 25, 'bold'),
                        bg="light blue")
    result_text.place(relx=0.5, rely=0.2, anchor="center")

    # Closes the window and returns to menu
    def close():
        return_menu()
        result.destroy()

    def save_name():
        global name, score
        # If the name inputted is above 15 deletes any extra characters
        if len(name_entry.get()) > 15:
            name_entry.delete(15, END)

        name = name_entry.get()

        score = str(score)
        score = score.zfill(3)

        if not name_entry.get():
            pass
        # Appends the scores and name inputted
        # a text file for each difficulty
        else:
            if difficulty == "easy":
                file = open("easy_score.txt", "a")
                file.write(str(score) + " - " + name + "\n")
                file.close()
            elif difficulty == "medium":
                file = open("medium_score.txt", "a")
                file.write(str(score) + " - " + name + "\n")
                file.close()
            elif difficulty == "hard":
                file = open("hard_score.txt", "a")
                file.write(str(score) + " - " + name + "\n")
                file.close()

            close()

    # This text is displayed when countdown runs out
    # so doesn't give the option to save score
    if countdown == 0:
        result_text.config(text="Oh No!!!\n\n "
                                "You weren't able to "
                                "complete the level in time\n"
                                f"You were able to get a"
                                f" Total Score of {score}")
    # This text is displayed if
    # full set of images are answered
    else:
        result_text.config(text="Congratulations!!!\n\n You completed the "
                                f"level with {countdown} seconds left\n"
                                f" You got a Total Score of {score}")
        name_entry = Entry(result)
        name_entry.place(relx=0.5, rely=0.6, anchor="center")

        confirm_name = Button(result, text="Save Score", command=save_name)
        confirm_name.place(relx=0.5, rely=0.8, anchor="center")

    close_button = Button(result, text="Close Window", command=close)
    close_button.place(relx=0.5, rely=0.9, anchor="center")

    # Makes it so window can't be close normally.
    result.overrideredirect(True)


# Displays the top 3 scores from each difficulty.
def display_scores():
    global top_easy, top_medium, top_hard, sort_easy, sort_medium, sort_hard
    # Reads the text and puts it into a variable.
    file = open("easy_score.txt", "r")
    file_read = file.readlines()
    # Sorts the different scores
    # from highest to lowest
    sort_easy = sorted(file_read, reverse=True)

    file = open("medium_score.txt", "r")
    file_read = file.readlines()
    sort_medium = sorted(file_read, reverse=True)

    file = open("hard_score.txt", "r")
    file_read = file.readlines()
    sort_hard = sorted(file_read, reverse=True)

    # Makes it so only the 3 highest scores are displayed
    for i in sort_easy[0:3]:
        top_easy += i

    for i in sort_medium[0:3]:
        top_medium += i

    for i in sort_hard[0:3]:
        top_hard += i

    # Puts the scores onto the GUI.
    easy_high_score.config(text=f"{top_easy}")
    medium_high_score.config(text=f"{top_medium}")
    hard_high_score.config(text=f"{top_hard}")


# Puts all the different lengths of the fish in a nested list.
Fish_list = [["This Salmon is 33cm in length",
              "This Salmon is 0.7m in length",
              "This Salmon is 52cm in length",
              "This Salmon is 58cm in length"],
             ["This Tuna is 64cm in length",
              "This Tuna is 1m in length",
              "This Tuna is 0.5m in length",
              "This Tuna is 70cm in length"],
             ["This Cod is 22cm in length",
              "This Cod is 40cm in length",
              "This Cod is 0.2m in length",
              "This Cod is 31cm in length"],
             ["This Mackerel is 20cm in length",
              "This Mackerel 37cm is in length",
              "This Mackerel is 32cm in length",
              "This Mackerel is 0.4m in length"]]

# ----------------------Main Frame GUI------------------------
title_frame = tk.LabelFrame(main_frame, bg="blue")
title_frame.grid(row=0, column=0, columnspan=3, sticky="NSEW")

title_title_frame = tk.LabelFrame(title_frame, borderwidth=0)
title_title_frame.place(relx=0.5, rely=0.5, anchor="center")

title = tk.Label(title_title_frame, text="Fishing Game",
                 font=("Trebuchet MS", 50, 'bold'), bg="blue")
title.grid(row=0, column=0)

rules_frame = tk.LabelFrame(main_frame, bg="#4257f5")
rules_frame.grid(row=1, column=1, sticky="NSEW")

rules_title_frame = tk.LabelFrame(rules_frame, borderwidth=0)
rules_title_frame.place(relx=0.5, rely=0.1, anchor="center")

rules = tk.Label(rules_title_frame, text="Explanation",
                 font=("Trebuchet MS", 40, 'bold'), bg="#4257f5")
rules.grid(row=0, column=0)

explanation_frame = tk.LabelFrame(rules_frame, borderwidth=0)
explanation_frame.place(relx=0.5, rely=0.3, anchor="center")

explanation = tk.Label(explanation_frame,
                       text="In this game a series of "
                            "images of fish will be shown.\n "
                            "They will be accompanied by their length\n"
                            " and what type of fish they are.\n"
                            "Using the list of rules on the left hand side.\n"
                            "You must decide whether to"
                            " catch or release the fish.\n"
                            "Answering correctly will grant you score.\n"
                            "Try and compete to get a spot"
                            " one of the top scores!!!",
                            font=("Trebuchet MS", 22, 'bold'), bg="#4257f5")
explanation.grid(row=0, column=0)

# Difficulty Section
difficulty_frame = tk.LabelFrame(main_frame, bg="#21700d")
difficulty_frame.grid(row=1, column=2, sticky="NSEW")

difficulty_title_frame = tk.LabelFrame(difficulty_frame, borderwidth=0)
difficulty_title_frame.place(relx=0.5, rely=0.1, anchor="center")

difficulty_title = tk.Label(difficulty_title_frame, text="Difficulty",
                            font=("Trebuchet MS", 40, 'bold'), bg="#21700d")
difficulty_title.grid(row=0, column=0)

difficulty_button_1 = tk.Button(difficulty_frame, text="Easy",
                                font=("Trebuchet MS", 35, 'bold'), width=8,
                                command=easy)
difficulty_button_1.place(relx=0.5, rely=0.3, anchor="center")

difficulty_button_2 = tk.Button(difficulty_frame, text="Medium",
                                font=("Trebuchet MS", 35, 'bold'), width=8,
                                command=medium)
difficulty_button_2.place(relx=0.5, rely=0.4, anchor="center")

difficulty_button_3 = tk.Button(difficulty_frame, text="Hard",
                                font=("Trebuchet MS", 35, 'bold'), width=8,
                                command=hard)
difficulty_button_3.place(relx=0.5, rely=0.5, anchor="center")

# Scoreboard Section
high_score_frame = tk.LabelFrame(main_frame, bg="#21700d")
high_score_frame.grid(row=1, column=0, sticky="NSEW")

high_score_title = tk.Label(high_score_frame, text="High Scores",
                            font=("Trebuchet MS", 35, 'bold'), bg="#21700d")
high_score_title.place(relx=0.5, rely=0.1, anchor="center")

easy_title = tk.Label(high_score_frame, text="Easy",
                      font=("Trebuchet MS", 25, 'bold'), bg="#21700d")
easy_title.place(relx=0.5, rely=0.25, anchor="center")

easy_high_score = tk.Label(high_score_frame,
                           font=("Trebuchet MS", 20, 'bold'), bg="#21700d")
easy_high_score.place(relx=0.5, rely=0.38, anchor="center")

medium_title = tk.Label(high_score_frame, text="Medium",
                        font=("Trebuchet MS", 25, 'bold'), bg="#21700d")
medium_title.place(relx=0.5, rely=0.5, anchor="center")

medium_high_score = tk.Label(high_score_frame,
                             font=("Trebuchet MS", 20, 'bold'), bg="#21700d")
medium_high_score.place(relx=0.5, rely=0.63, anchor="center")

hard_title = tk.Label(high_score_frame, text="Hard",
                      font=("Trebuchet MS", 25, 'bold'), bg="#21700d")
hard_title.place(relx=0.5, rely=0.75, anchor="center")

hard_high_score = tk.Label(high_score_frame,
                           font=("Trebuchet MS", 20, 'bold'), bg="#21700d")
hard_high_score.place(relx=0.5, rely=0.88, anchor="center")

# Configures the columns and rows to
# align the frames properly for the main menu.
main_frame.columnconfigure(0, weight=2)
main_frame.columnconfigure(1, weight=5)
main_frame.columnconfigure(2, weight=2)
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=4)

# ---------------------Fishing Game GUI----------------------
game_top_frame = tk.LabelFrame(fishing_frame, bg="blue")
game_top_frame.grid(row=0, column=0, columnspan=3, sticky="NSEW")

game_top = tk.LabelFrame(game_top_frame, borderwidth=0)
game_top.place(relx=0.5, rely=0.5, anchor="center")

game_title = tk.Label(game_top, text="Fishing Game",
                      font=("Trebuchet MS", 50, 'bold'), bg="blue")
game_title.grid(row=0, column=0)

instructions_frame = tk.LabelFrame(fishing_frame, bg="#21700d")
instructions_frame.grid(row=1, column=0, sticky="NSEW")

instruct_frame = tk.LabelFrame(instructions_frame, borderwidth=0)
instruct_frame.place(relx=0.5, rely=0.4, anchor="center")

instruct_title = tk.Label(instruct_frame,
                          text="1.Salmon must be at least\n 55cm"
                               " in length to catch \n\n"
                               "2.Tuna must be at least\n 69cm"
                               " in length to catch\n\n"
                               "3.Mackerel must be at least\n 28cm"
                               " in length to catch\n\n"
                               "4.Cod must be at least\n 33cm"
                               " in length to catch\n\n",
                          font=("Trebuchet MS", 20, 'bold'), bg="#21700d")
instruct_title.grid(row=0, column=0)

# Game-play section
play_frame = tk.LabelFrame(fishing_frame, bg="#4257f5")
play_frame.grid(row=1, column=1, sticky="NSEW")

game_countdown = tk.Label(game_top_frame, bg="blue",
                          text=f"Time:{countdown}",
                          font=("Trebuchet MS", 35, 'bold'))
game_countdown.place(relx=0.9, rely=0.5, anchor="center")

image_frame = tk.LabelFrame(play_frame, borderwidth=0)
image_frame.place(relx=0.5, rely=0.4, anchor="center")

image_game = tk.Label(image_frame, borderwidth=0)
image_game.grid(row=0, column=0)

play_game_frame = tk.LabelFrame(play_frame, borderwidth=0)
play_game_frame.place(relx=0.5, rely=0.8, anchor="center")

text_game = tk.Label(play_game_frame,
                     font=("Trebuchet MS", 20, 'bold'), bg="#4257f5")
text_game.grid(row=0, column=0)

options_frame = tk.LabelFrame(fishing_frame, bg="#21700d")
options_frame.grid(row=1, column=2, sticky="NSEW")

game_score = tk.Label(options_frame, bg="#21700d",
                      text=f"Score:{score}",
                      font=("Trebuchet MS", 35, 'bold'))
game_score.place(relx=0.5, rely=0.1, anchor="center")

# Buttons
catch_button = tk.Button(options_frame, text="Catch",
                         font=("Trebuchet MS", 35, 'bold'),
                         width=8, height=2,
                         command=catch)
catch_button.place(relx=0.5, rely=0.25, anchor="center")

release_button = tk.Button(options_frame, text="Release",
                           font=("Trebuchet MS", 35, 'bold'),
                           width=8, height=2,
                           command=release)
release_button.place(relx=0.5, rely=0.45, anchor="center")

return_button = tk.Button(options_frame, text="Menu",
                          font=("Trebuchet MS", 35, 'bold'), width=8,
                          command=return_menu)
return_button.place(relx=0.5, rely=0.9, anchor="center")

# Configures the columns and rows to
# align the frames properly for fishing frame.
fishing_frame.columnconfigure(0, weight=2)
fishing_frame.columnconfigure(1, weight=5)
fishing_frame.columnconfigure(2, weight=2)
fishing_frame.rowconfigure(0, weight=1)
fishing_frame.rowconfigure(1, weight=4)

display_scores()
main_frame.pack(fill="both", expand=1)
root.mainloop()
