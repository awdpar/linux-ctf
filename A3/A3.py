# CTF Python Game
# Basic Linux Commands (pwd, ls, cat)

import os

def main():
    leaderboard = {}

    print("=== Linux Basics CTF ===")

    while True:
        name = input("\nEnter student name: ").strip()

        score = 0
        score += question_one()
        score += question_two()

        leaderboard[name] = score
        print(f"\n{name}'s total score: {score}")

        player2 = input("\nIs there another player? (y/n): ").strip().lower()
        if player2 != "y":
            break


#Question 1
def question_one():
    print("\n--- Question 1 ---")
    print("Find the flag inside the file list system using the right command")

    user_flag = input("\nEnter the flag: ").strip()

    if user_flag == "FLAG{YOUFOUNDLSFLAG}":
        print("Correct flag!")
        return 10
    else:
        print("Incorrect flag.")
        return 0
    
#Question 2
def question_two():
    print("\n--- Question 2 ---")
    print("Find the flag inside the file named 'flag2.txt' using the right command")

    user_flag = input("\nEnter the flag: ").strip()

    if user_flag == "FLAG{A3Q2ANSFOUND}":
        print("Correct flag!")
        return 10
    else:
        print("Incorrect flag.")
        return 0


if __name__ == "__main__":
    main()