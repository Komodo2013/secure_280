# Used to run math.log to find column width
import math

# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
formats = {
    "green": "\x1b[0;92;48m",
    "white": "\x1b[0;97;48m"
}


# Wrapper of print and set_format
# @param s String message to print to terminal and gets user input
# @returns in String whatever the user typed
def get_input(s=""):
    return input(formats["white"] + s + "\t\u2192 ").strip()


# Ask for the dimensions of the multiplication table to generate
columns = int(get_input("How many columns?"))
rows = int(get_input("How many rows?"))

# Calculate width of max number column by multiplying to get max, and taking log10
width = int(math.log(rows * columns, 10)) + 2  # add 2, one for whitespace and 1 for the first digit

# for each row
for x in range(1, rows + 1):  # added 1 since index != 0 at start

    # for each column
    for y in range(1, columns + 1):  # added 1 since index != 0 at start
        # If to make first row and column green as headers, rest white
        if y != 1 and x != 1:
            print(f"{formats['white']}", end='')
        else:
            print(f"{formats['green']}", end='')

        # Print the value with precalculated spacing
        print(f"{x * y: {width}}", end='')

    # new line
    print("")
