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
import pty
import threading
import re

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
total_questions = 0

# Correct Flags
FLAGS = {
    1: "FLAG{YOUFOUNDLSFLAG}",
    2: "FLAG{A3Q2ANSFOUND}",
    3: "FLAG{suspicious_activity}"
    #3: "FLAG{EXAMPLEFLAG}"                                                                 #UPDATE THIS FOR MORE QUESTIONS
}

# Root window
root = Tk()
root.title("Linux Basics CTF")
root.geometry("1000x800")
root.minsize(900, 700)
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
    font=("Courier New", 25),
    fg="#0a3", 
    bg="#0b0b0b"
)
#3d logo
logo_shadow.place(x=3, y=3)

logo = Label(
    header, 
    text=linux_title,
    font=("Courier New", 25),
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
middle.grid_columnconfigure(0, weight=0, minsize=260)
middle.grid_columnconfigure(1, weight=2)

# Left panel
left_panel = Frame(middle, bg="#111")
left_panel.grid(row=0, column=0, sticky="ns", padx=(0, 10))

left_panel.grid_propagate(False)
left_panel.config(width=260)

    # Left panel contents
def styled_entry(parent):
    return Entry(
        parent,
        bg="#000",
        fg="#00ff66",
        insertbackground="#00ff66",
        relief="flat",
        width=38,
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

Label(
    left_panel,
    text="Number of Questions",
    bg="#111",
    fg="#00ff66",
    font=("Courier New", 11)
).pack(pady=(10, 3))

question_count_entry = styled_entry(left_panel)
question_count_entry.pack(fill="x", padx=10)

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
submit_btn.config(state="disabled")
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
    wraplength=500,
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
    font=("Courier New", 12),
    relief="flat"
)
terminal.grid(row=0, column=0, sticky="nsew")

# ----------------------------
# REAL TERMINAL USING PTY
# ----------------------------

# Create sandbox directory
CTF_DIR = os.path.abspath("ctf_env")

if not os.path.exists(CTF_DIR):
    os.makedirs(CTF_DIR)

#challenge files
with open(os.path.join(CTF_DIR, "flag.txt"), "w") as f:
    f.write("FLAG{YOUFOUNDLSFLAG}\n")

os.makedirs(os.path.join(CTF_DIR, "A3/Question2"), exist_ok=True)

with open(os.path.join(CTF_DIR, "A3/Question2/flag1.txt"), "w") as f:
    f.write("FLAG{A3Q2ANSFOUND}\n")

with open(os.path.join(CTF_DIR, "A3/forensics.txt"), "w") as f:
    f.write("RkxBR3tzdXNwaWNpb3VzX2FjdGl2aXR5fQ==\n")

os.chdir(CTF_DIR)

# Start bash shell
master_fd, slave_fd = pty.openpty()

pid = os.fork()

if pid == 0:
    os.setsid()
    os.dup2(slave_fd, 0)
    os.dup2(slave_fd, 1)
    os.dup2(slave_fd, 2)

    os.environ["TERM"] = "dumb"

    os.execvp("bash", ["bash", "--noprofile", "--norc"])

# Customize prompt
os.write(master_fd, b'stty -echo\n')
os.write(master_fd, b'PS1="student@linux-ctf:\\w$ "\n')
os.write(master_fd, b'clear\n')

# Remove ANSI escape sequences (fixes Linux weird characters)
ansi_escape = re.compile(
    r'(\x1B[@-_][0-?]*[ -/]*[@-~])'  
    r'|\x1B\][^\x07]*\x07'            
    r'|\x1B\[[0-9;]*[a-zA-Z]'         
    r'|\x07'                           
    r'|\x0f'                           
    r'|\x0e'                           
    r'|\r'                             
)

def clean_ansi(text):
    return ansi_escape.sub('', text)

# Read shell output in background thread
def read_from_shell():
    while True:
        try:
            output = os.read(master_fd, 1024).decode(errors="ignore")
            output = clean_ansi(output)  
            output = output.replace('\r\n', '\n').replace('\r', '\n')
            terminal.insert("end", output)
            terminal.see("end")
        except OSError:
            break

threading.Thread(target=read_from_shell, daemon=True).start()

def clear_startup_noise():
    import time
    time.sleep(0.8)
    terminal.delete("1.0", "end")
    time.sleep(0.3)
    os.write(master_fd, b'\n')

threading.Thread(target=clear_startup_noise, daemon=True).start()

# Send user input to shell
def handle_terminal_input(event):
    line = terminal.get("insert linestart", "insert")

    if "$ " in line:
        command = line.split("$ ")[-1].strip()
    else:
        command = line.strip()

    terminal.insert("end", "\n")

    if command == "clear":
        terminal.delete("1.0", "end")
        os.write(master_fd, b'\n')  #refresh prompt
        return "break"

    os.write(master_fd, (command + "\n").encode())
    return "break"


terminal.bind("<Return>", handle_terminal_input)


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
    global current_player, current_score, question_number, total_questions

    current_player = name_entry.get().strip()
    if not current_player:
        messagebox.showerror("Error", "Enter a student name")
        return
    try:
        total_questions = int(question_count_entry.get().strip())
        if total_questions < 1:
            raise ValueError
        if total_questions > 3:                                                             #UPDATE THIS FOR MORE QUESTIONS
            messagebox.showerror("Error", f"Choose a number under 3")
            return
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number of questions")
        return

    current_score = 0
    question_number = 1

    name_entry.config(state="disabled")
    question_count_entry.config(state="disabled")

    show_question()
    submit_btn.config(state="normal")
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
    elif question_number == 3:
        question_label.config(
            text="Question 2:\n*Decode* the flag in forensics.txt in base64 using echo"
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

    if question_number > total_questions:                                                   
        end_player()
    else:
        show_question()

def update_status():
    status.config(text=f"Score: {current_score} | Question {question_number}/{total_questions}")

def end_player():
    submit_btn.config(state="disabled")

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
    submit_btn.config(state="disabled")

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