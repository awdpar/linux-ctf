# Parampal Sandhu | First Internship Project | Start Date: 1/13/2026
#
# Kali/Linux/Raspberry PI platform in Python
# High School Students can compete with each other
# Basic Linux commands like pwd/ls
# 
# Currently the program allows one player so the first player
#  goes and gets their score then the second player replays the
#  game and gets their score. The one with the higher score wins.

def main():
    print("==== Linux Command Challenge ====")
    name = input("Enter your name: ").strip()

    score = linuxQuiz()

    print(f"\n{name}, your final score is: {score}")

def linuxQuiz():
    score = 0

    #question 1
    print("\nQuestion 1:")
    print("Which command shows your current directory?")
    answer = input("Your answer: ").strip()

    if answer == "pwd":
        print("Correct!")
        score += 1
    else:
        print("Wrong. Correct answer is: pwd")

    #question 2
    print("\nQuestion 2:")

    #return score
    return score

#save score to file


if __name__ == "__main__":
    main()
