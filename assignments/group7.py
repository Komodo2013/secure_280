# Used to generate a random num
from random import randint

# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
formats = {
    "SYS": "\x1b[0;97;48m",
    "yellow": "\x1b[0;93;48m",
}


# Wrapper of input, just with formatting
# @param s String message to print to terminal and gets user input
# @returns in String whatever the user typed
def get_input(s=""):
    return input(formats["SYS"] + s + "\t\u2192 ").strip()


high_score = 10 ** 7    # used to display high score. big number artificially declared
continuing = True       # controls the while loop for each round of the game
difficulty = int(get_input("Enter difficulty from 1-10"))  # Used to change how hard the game is


while continuing:
    # used to inflate the difficulty of the game 1 = 10 and 10 = 1000
    secret = randint(1, 10 * difficulty ** 2)
    # prints the range  of numbers that the secret may be in
    print(f"Generated number between {formats['yellow']}0{formats['SYS']} and {formats['yellow']}{difficulty ** 3}"
          f"{formats['SYS']}\n")
    # first attempt
    answer = int(get_input("What's your guess? "))
    guesses = 1
    # while the guesses are incorrect
    while not answer == secret:
        # give a hint
        if answer > secret:
            print("Your guess is high\n")
        else:
            print("Your guess is low\n")

        guesses += 1
        answer = int(get_input("What's your new guess? "))
        # end loop

    # display guesses
    print(f"\nCongrats you guessed it in {formats['yellow']}{guesses}{formats['SYS']} attempts!")
    # save the guess score if its new best
    if guesses < high_score: high_score = guesses
    # display best game score
    print(f"Your high score: {formats['yellow']}{high_score}{formats['SYS']}")

    # should we loop to next game
    continuing = "yes" in get_input("\nTry again? (yes/no)").lower()

# close
print("Bye")
