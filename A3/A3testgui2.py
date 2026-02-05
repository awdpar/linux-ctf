# CTF Python Game
# Basic Linux Commands (pwd, ls, cat)
#
# (V2) Full screen application with built-in terminal emulator updated from previous version
#  that used computers terminal in a seperate window.

import tkinter as tk
from tkinter import messagebox
from tkinter import *
import subprocess
import platform
import os

linux_title = """
██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗
██║     ██║████╗  ██║██║   ██║╚██╗██╔╝
██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝ 
██║     ██║██║╚██╗██║██║   ██║ ██╔██╗ 
███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗
╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝
"""

# Game data
leaderboard = {}
current_score = 0
current_player = ""
question_number = 1
current_dir = "/home/student"

# Correct Flags
FLAGS = {
    1: "FLAG{YOUFOUNDLSFLAG}",
    2: "FLAG{A3Q2ANSFOUND}",
    #3: "FLAG{EXAMPLEFLAG}"                                                                 #UPDATE THIS FOR MORE QUESTIONS
}

# Root window
root = Tk()
root.title("Linux Basics CTF")
root.geometry("900x650")
root.minsize(800, 550)
root.configure(bg="#0b0b0b")

# *ROOT GRID CONFIG*
# Row 0 = Header (logo)
# Row 1 = Controls / Question
# Row 2 = Terminal
# Row 3 = Status bar
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=1)  # terminal expands
root.grid_rowconfigure(3, weight=0)

root.grid_columnconfigure(0, weight=1)

# Logo
header = Frame(root, bg="#0b0b0b")
header.grid(row=0, column=0, pady=10)

logo_shadow = Label(
    header, 
    text=linux_title,
    font=("Courier New", 26),
    fg="#0a3", 
    bg="#0b0b0b"
)
#3d logo
logo_shadow.place(x=3, y=3)

logo = Label(
    header, 
    text=linux_title,
    font=("Courier New", 26),
    fg="#00ff66", 
    bg="#0b0b0b"
)
logo.pack()

# Middle panel (left+right)
middle = Frame(root, bg="#0b0b0b")
middle.grid(row=1, column=0, sticky="nsew", padx=20)

# Two columns:
# col 0 = player / buttons
# col 1 = questions
middle.grid_columnconfigure(0, weight=1)
middle.grid_columnconfigure(1, weight=2)

# Left panel
left_panel = Frame(middle, bg="#111")
left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    # Left panel contents
def styled_entry(parent):
    return Entry(
        parent,
        bg="#000",
        fg="#00ff66",
        insertbackground="#00ff66",
        relief="flat",
        font=("Courier New", 11)
    )

def styled_button(parent, text, cmd):
    return Button(
        parent,
        text=text,
        command=cmd,
        bg="#111",
        fg="#00ff66",
        activebackground="#00ff66",
        activeforeground="#000",
        relief="flat",
        font=("Courier New", 11),
        pady=6
    )

Label(
    left_panel, 
    text="Student Name", 
    bg="#111", 
    fg="#00ff66", 
    font=("Courier New", 11)
).pack(pady=(10, 3))

name_entry = styled_entry(left_panel)
name_entry.pack(fill="x", padx=10)

start_btn = styled_button(left_panel, "Start Game", lambda: start_game())
start_btn.pack(pady=10, padx=10, fill="x")

Label(
    left_panel, 
    text="Enter Flag", 
    bg="#111", 
    fg="#00ff66", 
    font=("Courier New", 11)
).pack(pady=(10, 3))

flag_entry = styled_entry(left_panel)
flag_entry.pack(fill="x", padx=10)

submit_btn = styled_button(left_panel, "Submit Flag", lambda: submit_flag())
submit_btn.pack(pady=10, padx=10, fill="x")

# Right panel
right_panel = Frame(middle, bg="#111")
right_panel.grid(row=0, column=1, sticky="nsew")

    # Right panel contents
question_label = Label(
    right_panel,
    text="",
    bg="#111",
    fg="#e6e6e6",
    justify="left",
    wraplength=400,
    font=("Courier New", 14)
)
question_label.pack(padx=10, pady=10, anchor="nw")

# Terminal
terminal_frame = Frame(root, bg="#000")
terminal_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

terminal_frame.grid_rowconfigure(0, weight=1)
terminal_frame.grid_columnconfigure(0, weight=1)

terminal = Text(
    terminal_frame,
    bg="#000",
    fg="#00ff66",
    insertbackground="#00ff66",
    font=("Courier New", 11),
    relief="flat"
)
terminal.grid(row=0, column=0, sticky="nsew")

current_dir = "/home/student"

def get_prompt():
    display_dir = current_dir.replace("/home/student", "~")
    return f"student@linux-ctf:{display_dir}$ "

terminal.insert("end", get_prompt())

#             1
def handle_terminal_input(event):
    line = terminal.get("insert linestart", "insert").strip()

    cmd = line.replace(get_prompt(), "")

    terminal.insert("end", "\n")
    process_command(cmd)

    terminal.insert("end", get_prompt())
    terminal.see("end")

    return "break"

terminal.bind("<Return>", handle_terminal_input)

#               2
def process_command(cmd):
    global current_dir

    cmd = cmd.strip()

    if cmd == "ls":
        if current_dir == "/home/student":
            terminal.insert("end", "A3  Documents  Downloads flag.txt FLAG{YOUFOUNDLSFLAG}\n")
        elif current_dir == "/home/student/A3":
            terminal.insert("end", "Question2\n")
        elif current_dir == "/home/student/A3/Question2":
            terminal.insert("end", "flag1.txt\n")
        else:
            terminal.insert("end", "\n")

    elif cmd.startswith("cd"):
        parts = cmd.split()

        if len(parts) == 1 or parts[1] == "~":
            current_dir = "/home/student"

        elif parts[1] == "..":
            if current_dir != "/home/student":
                current_dir = "/".join(current_dir.split("/")[:-1])

        else:
            new_path = current_dir + "/" + parts[1]

            if new_path in [
                "/home/student/A3",
                "/home/student/A3/Question2"
            ]:
                current_dir = new_path
            else:
                terminal.insert("end", "cd: no such file or directory\n")

    elif cmd.startswith("cat"):
        if current_dir == "/home/student/A3/Question2" and "flag1.txt" in cmd:
            terminal.insert("end", "FLAG{A3Q2ANSFOUND}\n")
        else:
            terminal.insert("end", "cat: file not found\n")

    elif cmd == "pwd":
        terminal.insert("end", current_dir + "\n")

    elif cmd == "clear":
        terminal.delete("1.0", "end")

    elif cmd == "":
        pass

    else:
        terminal.insert("end", f"{cmd}: command not found\n")

# Status bottom left
status = Label(
    root,
    text="Score: 0 | Question 1",
    bg="#111",
    fg="#00ff66",
    anchor="w",
    padx=10,
    font=("Courier New", 10)
)
status.grid(row=3, column=0, sticky="ew")

# Game functions
def start_game():
    global current_player, current_score, question_number

    current_player = name_entry.get().strip()
    if not current_player:
        messagebox.showerror("Error", "Enter a student name")
        return

    current_score = 0
    question_number = 1

    name_entry.config(state="disabled")

    show_question()
    update_status()

def show_question():
    if question_number == 1:
        question_label.config(
            text="Question 1:\nFind the flag using the ls command"
        )
    elif question_number == 2:
        question_label.config(
            text="Question 2:\nFind the flag inside A3/Question2/flag1.txt using cat"
        )
    #elif question_number == 3:
    #    question_label.config(
    #        text="Question 3:Find the flag in your current directory"
    #    )
                                                                                            #UPDATE THIS FOR MORE QUESTIONS

def submit_flag():
    global current_score, question_number

    user_flag = flag_entry.get().strip()

    if user_flag == FLAGS.get(question_number):
        current_score += 10
        messagebox.showinfo("Correct", "Correct flag!")
    else:
        messagebox.showerror("Incorrect", "Incorrect flag")

    flag_entry.delete(0, END)
    question_number += 1
    update_status()

    if question_number > 2:                                                                 #UPDATE THIS FOR MORE QUESTIONS
        end_player()
    else:
        show_question()

def update_status():
    status.config(text=f"Score: {current_score} | Question {question_number}")

def end_player():
    leaderboard[current_player] = current_score

    again_player = messagebox.askyesno(
        "Player Finished",
        f"{current_player} scored {current_score}.\n\nIs there another player?"
    )

    if again_player:
        reset_for_next_player()
    else:
        show_leaderboard()

def reset_for_next_player():
    global current_player, current_score, question_number

    current_player = ""
    current_score = 0
    question_number = 1

    name_entry.config(state="normal")
    name_entry.delete(0, END)

    flag_entry.delete(0, END)
    question_label.config(text="")

    update_status()

    terminal.delete("1.0", "end")
    terminal.insert("end", "student@linux-ctf:~$ ")

def show_leaderboard():
    results = "Final Leaderboard\n\n"

    for name, score in leaderboard.items():
        results += f"{name}: {score}\n"

    messagebox.showinfo("Leaderboard", results)
    root.quit()

# Start app
root.mainloop()