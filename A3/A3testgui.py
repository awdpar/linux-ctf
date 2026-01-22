import tkinter as tk
from tkinter import messagebox
from tkinter import *

# Game data
leaderboard = {}
current_score = 0
current_player = ""
question_number = 1

# Correct flags
FLAGS = {
    1: "FLAG{YOUFOUNDLSFLAG}",
    2: "FLAG{A3Q2ANSFOUND}"
}

def start_game():
     
    global current_player, current_score, question_number
    current_player = name_entry.get().strip()
    if not current_player:
        messagebox.showerror("Error", "Enter a student name")
        return

    current_score = 0
    question_number = 1
    name_entry.config(state="disabled")
    start_btn.config(state="disabled")
    show_question()

def show_question():
    question_label.config(
        text=f"Question {question_number}:\n"
             + ("Find the flag using the ls command"
                if question_number == 1
                else "Find the flag inside A3/Question2/flag1.txt using cat")
    )
    flag_entry.delete(0, tk.END)

def submit_flag():
    global current_score, question_number

    user_flag = flag_entry.get().strip()

    if user_flag == FLAGS[question_number]:
        current_score += 10
        messagebox.showinfo("Correct", "Correct flag!")
    else:
        messagebox.showerror("Incorrect", "Incorrect flag")

    question_number += 1

    if question_number > 2:
        end_player()
    else:
        show_question()

def end_player():
    leaderboard[current_player] = current_score
    messagebox.showinfo(
        "Player Finished",
        f"{current_player}'s Score: {current_score}"
    )

    again = messagebox.askyesno("Next Player", "Is there another player?")
    if again:
        reset_for_next_player()
    else:
        show_leaderboard()

def reset_for_next_player():
    name_entry.config(state="normal")
    name_entry.delete(0, tk.END)
    start_btn.config(state="normal")
    question_label.config(text="")
    flag_entry.delete(0, tk.END)

def show_leaderboard():
    results = "Final Leaderboard\n\n"
    for name, score in leaderboard.items():
        results += f"{name}: {score}\n"

    messagebox.showinfo("Leaderboard", results)
    root.quit()

# GUI Setup
root = tk.Tk()
root.title("Linux CTF")
root.geometry("400x300")

tk.Label(root, text="Linux Basics CTF", font=("Arial", 20)).pack(pady=10)

#image
#image = PhotoImage(file="linux.png")
#image_label = tk.Label(root, image=image)
#image_label.pack()
#image = resizeImage(image, 150, 150)

tk.Label(root, text="Student Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

start_btn = tk.Button(root, text="Start Game", command=start_game)
start_btn.pack(pady=5)

question_label = tk.Label(root, text="", wraplength=350)
question_label.pack(pady=10)

flag_entry = tk.Entry(root)
flag_entry.pack()

submit_btn = tk.Button(root, text="Submit Flag", command=submit_flag)
submit_btn.pack(pady=10)

root.mainloop()
