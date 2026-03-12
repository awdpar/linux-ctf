# CTF Python Game
# Basic Linux Commands (pwd, ls, cat, grep, mkdir)
# 
# (V2) Full screen application with built-in terminal emulator updated from previous version
#  that didn't have buttons to skip around the questions.

from tkinter import messagebox
from tkinter import *
import os
import shutil
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
total_questions = 0
answered_questions = set()
wrong_questions = set()

# Correct Flags
FLAGS = {
    1: "FLAG{YOUFOUNDLSFLAG}",
    2: "FLAG{A3Q2ANSFOUND}",
    3: "FLAG{suspicious_activity}",
    4: "FLAG{GREPFOUND}",
    5: None,  # in submit_flag
    6: "FLAG{CHMOD_UNLOCKED}",   
                                                                                            #UPDATE THIS FOR MORE QUESTIONS
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
root.grid_rowconfigure(2, weight=1)
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
logo_shadow.place(x=3, y=3)

logo = Label(
    header,
    text=linux_title,
    font=("Courier New", 25),
    fg="#00ff66",
    bg="#0b0b0b"
)
logo.pack()

# Middle panel (left&right)
middle = Frame(root, bg="#0b0b0b")
middle.grid(row=1, column=0, sticky="nsew", padx=20)

middle.grid_columnconfigure(0, weight=0, minsize=260)
middle.grid_columnconfigure(1, weight=2)

# Left panel
left_panel = Frame(middle, bg="#111")
left_panel.grid(row=0, column=0, sticky="ns", padx=(0, 10))

left_panel.grid_propagate(False)
left_panel.config(width=260)

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

# Question row
indicator_frame = Frame(right_panel, bg="#111")
indicator_frame.pack(padx=10, pady=(8, 0), anchor="nw")

indicator_labels = {}

question_label = Label(
    right_panel,
    text="",
    bg="#111",
    fg="#e6e6e6",
    justify="left",
    wraplength=500,
    font=("Courier New", 14)
)
question_label.pack(padx=10, pady=(6, 4), anchor="nw")

# Question arrows
nav_frame = Frame(right_panel, bg="#111")
nav_frame.pack(side="bottom", padx=10, pady=(0, 8), anchor="center")

prev_btn = Button(
    nav_frame,
    text="←",
    command=lambda: navigate(-1),
    bg="#111",
    fg="#00ff66",
    activebackground="#00ff66",
    activeforeground="#000",
    relief="flat",
    font=("Courier New", 16),
    state="disabled"
)
prev_btn.pack(side="left", padx=(0, 6))

next_btn = Button(
    nav_frame,
    text="→",
    command=lambda: navigate(1),
    bg="#111",
    fg="#00ff66",
    activebackground="#00ff66",
    activeforeground="#000",
    relief="flat",
    font=("Courier New", 16),
    state="disabled"
)
next_btn.pack(side="left")

# Terminal
terminal_frame = Frame(root, bg="#000")
terminal_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10,20))

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

# PTY
# create sandbox
CTF_DIR = os.path.abspath("ctf_env")

if os.path.exists(CTF_DIR):
    shutil.rmtree(CTF_DIR)
os.makedirs(CTF_DIR)

# Q1
open(os.path.join(CTF_DIR, "FLAG{YOUFOUNDLSFLAG}"), "w").close()

# Q2
os.makedirs(os.path.join(CTF_DIR, "A3/Question2"), exist_ok=True)
with open(os.path.join(CTF_DIR, "A3/Question2/flag1.txt"), "w") as f:
    f.write("FLAG{A3Q2ANSFOUND}\n")

# Q3
with open(os.path.join(CTF_DIR, "A3/forensics.txt"), "w") as f:
    f.write("RkxBR3tzdXNwaWNpb3VzX2FjdGl2aXR5fQ==\n") 

# Q4
os.makedirs(os.path.join(CTF_DIR, "logs"), exist_ok=True)
with open(os.path.join(CTF_DIR, "logs/system.log"), "w") as f:
    f.write("INFO: system boot complete\n")
    f.write("INFO: user login successful\n")
    f.write("WARNING: disk usage at 80%\n")
    f.write("INFO: network interface up\n")
    f.write("FLAG{GREPFOUND}\n")
    f.write("ERROR: failed to mount /dev/sdb\n")
    f.write("INFO: cron job started\n")
    f.write("WARNING: high memory usage detected\n")

# Q5
os.makedirs(os.path.join(CTF_DIR, "challenge"), exist_ok=True)
with open(os.path.join(CTF_DIR, "challenge/README.txt"), "w") as f:
    f.write("Create a directory with any name you choose using mkdir.\n")
    f.write("Run: mkdir challenge/<yourname>\n")
    f.write("Then submit that directory name as your flag.\n")

# Q6
os.makedirs(os.path.join(CTF_DIR, "scripts"), exist_ok=True)
script_path = os.path.join(CTF_DIR, "scripts/reveal.sh")
with open(script_path, "w") as f:
    f.write("#!/bin/bash\n")
    f.write('echo "FLAG{CHMOD_UNLOCKED}"\n')
os.chmod(script_path, 0o644)

os.chdir(CTF_DIR)

# Start bash shell
master_fd, slave_fd = pty.openpty()

pid = os.fork()

if pid == 0:
    os.setsid()
    os.dup2(slave_fd, 0)
    os.dup2(slave_fd, 1)
    os.dup2(slave_fd, 2)

    os.environ["TERM"] = "xterm"

    os.execvp("bash", ["bash", "--noprofile", "--norc"])

# Customize prompt
os.write(master_fd, b'PS1="student@linux-ctf:\\w$ "\n')
os.write(master_fd, b'clear\n')

# Remove ANSI
ansi_escape = re.compile(
    r'(\x1B[@-_][0-?]*[ -/]*[@-~])'
    r'|\x1B\][^\x07]*\x07'
    r'|\x1B\[[0-9;]*[a-zA-Z]'
    r'|\x07'
    r'|\x0f'
    r'|\x0e'
    r'|\r'
    r'|\x7f'
    r'|\x08'
)

def clean_ansi(text):
    return ansi_escape.sub('', text)

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

def handle_terminal_input(event):
    line = terminal.get("insert linestart", "insert")
    command = line.split("$ ")[-1].strip() if "$ " in line else line.strip()

    if command == "clear":
        os.write(master_fd, b'\n')
        terminal.after(100, lambda: terminal.delete("1.0", "end"))
        terminal.after(200, lambda: os.write(master_fd, b'\n'))
        return "break"

    os.write(master_fd, b'\n')
    return "break"

def handle_terminal_keypress(event):
    if event.keysym == "BackSpace":
        os.write(master_fd, b'\x08')
        return
    if event.keysym == "Tab":
        os.write(master_fd, b'\t')
        return "break"
    if event.keysym == "c" and (event.state & 0x4):
        os.write(master_fd, b'\x03')
        return "break"
    if event.char and event.char.isprintable():
        os.write(master_fd, event.char.encode())
        return "break"

terminal.bind("<Return>", handle_terminal_input)
terminal.bind("<Key>", handle_terminal_keypress)

# Game functions
def build_indicators():
    for widget in indicator_frame.winfo_children():
        widget.destroy()
    indicator_labels.clear()
    for i in range(1, total_questions + 1):
        lbl = Label(
            indicator_frame,
            text=f" Q{i} ",
            bg="#111",
            fg="#444",
            font=("Courier New", 10, "bold"),
            padx=2
        )
        lbl.pack(side="left")
        indicator_labels[i] = lbl
    update_indicators()

def update_indicators():
    for i, lbl in indicator_labels.items():
        if i in answered_questions:
            if i == question_number:
                lbl.config(fg="#00ff66", bg="#003300")   # current + correct = green glow
            else:
                lbl.config(fg="#00ff66", bg="#111")        # correct = green
        elif i in wrong_questions:
            if i == question_number:
                lbl.config(fg="#ff3333", bg="#330000")   # current + wrong = red glow
            else:
                lbl.config(fg="#ff3333", bg="#111")        # wrong = red
        elif i == question_number:
            lbl.config(fg="#ffffff", bg="#333333")       # current unanswered = grey glow
        else:
            lbl.config(fg="#444", bg="#111")                 # unanswered

def navigate(direction):
    global question_number
    new_q = question_number + direction
    if 1 <= new_q <= total_questions:
        question_number = new_q
        show_question()
        update_indicators()
        update_nav_buttons()

        if question_number in answered_questions or question_number in wrong_questions:
            submit_btn.config(state="disabled")
        else:
            submit_btn.config(state="normal")

def update_nav_buttons():
    prev_btn.config(state="normal" if question_number > 1 else "disabled")
    next_btn.config(state="normal" if question_number < total_questions else "disabled")

def start_game():
    global current_player, current_score, question_number, total_questions, answered_questions, wrong_questions

    current_player = name_entry.get().strip()
    if not current_player:
        messagebox.showerror("Error", "Enter a student name")
        return
    try:
        total_questions = int(question_count_entry.get().strip())
        if total_questions < 1:
            raise ValueError
        if total_questions > 6:                                                                             #UPDATE THIS FOR MORE QUESTIONS
            messagebox.showerror("Error", "Choose a number between 1 and 6")                                   # 
            return
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number of questions")
        return

    current_score = 0
    question_number = 1
    answered_questions = set()
    wrong_questions = set()

    name_entry.config(state="disabled")
    question_count_entry.config(state="disabled")

    build_indicators()
    show_question()
    submit_btn.config(state="normal")
    update_nav_buttons()

def show_question():
    questions = {
        1: "Question 1:\nFind the flag using the ls command.",
        2: "Question 2:\nFind the flag inside A3/Question2/flag1.txt using cat.",
        3: "Question 3:\nDecode the flag in A3/forensics.txt.\n\nHint: echo <contents> | base64 -d",
        4: "Question 4:\nA flag is hidden somewhere in logs/system.log.\n\nHint: Use grep to search for FLAG{ in the file.",
        5: "Question 5:\nRead challenge/README.txt for your instructions.",
        6: "Question 6:\nThere is a script at scripts/reveal.sh that contains a flag but it won't run.\n\n"
                "Give it execute permission first, then run it.\n\nHint: chmod +x scripts/reveal.sh\nThen: ./scripts/reveal.sh"
    }                                                                                                       #UPDATE THIS FOR MORE QUESTIONS
    text = questions.get(question_number, "")
    if question_number in answered_questions:
        text += "\n\n✓ Already answered"
    elif question_number in wrong_questions:
        text += "\n\n✗ Incorrect, no more attempts"
    question_label.config(text=text)

def submit_flag():
    global current_score

    if question_number in answered_questions or question_number in wrong_questions:
        return

    user_flag = flag_entry.get().strip()
    correct = False

    if question_number == 5:
        challenge_dir = os.path.join(CTF_DIR, "challenge")
        dir_path = os.path.join(challenge_dir, user_flag)
        if os.path.isdir(dir_path):
            correct = True
        else:
            messagebox.showerror("Incorrect", "No directory with that name found in challenge/. Use mkdir first")
    elif user_flag == FLAGS.get(question_number):
        correct = True
    else:
        messagebox.showerror("Incorrect", "Incorrect flag")

    flag_entry.delete(0, END)

    if correct:
        current_score += 10
        answered_questions.add(question_number)
        messagebox.showinfo("Correct", "Correct flag!")
    else:
        wrong_questions.add(question_number)
        submit_btn.config(state="disabled")

    show_question()
    update_indicators()

    if len(answered_questions) + len(wrong_questions) >= total_questions:
        end_player()

def end_player():
    submit_btn.config(state="disabled")
    prev_btn.config(state="disabled")
    next_btn.config(state="disabled")

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
    global current_player, current_score, question_number, answered_questions, wrong_questions

    current_player = ""
    current_score = 0
    question_number = 1
    answered_questions = set()
    wrong_questions = set()

    name_entry.config(state="normal")
    name_entry.delete(0, END)
    question_count_entry.config(state="normal")
    question_count_entry.delete(0, END)

    flag_entry.delete(0, END)
    question_label.config(text="")
    submit_btn.config(state="disabled")
    prev_btn.config(state="disabled")
    next_btn.config(state="disabled")

    for widget in indicator_frame.winfo_children():
        widget.destroy()
    indicator_labels.clear()

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