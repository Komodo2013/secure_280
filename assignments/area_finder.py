import math


# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
formats = {
    "SYS": "0;97;48",
    "WARNING": "0;93;48",
    "ERROR": "0;91;48",
    "INFO": "0;96;48",
    "black": "0;97;40",
    "grey": "0;37;48",
    "red": "0;31;48",
    "green": "0;92;48",
    "yellow": "0;33;48",
    "blue": "0;94;48",
    "purple": "0;95;48",
    "cyan": "0;36;48",
    "white": "0;97;48"
}


# Simple function that formats future text a certain way
# @param format String the text format to be used defined as "int;int;int"
def set_format(style_type):
    print("\x1b[%sm" % style_type, end="")


# Wrapper of print and set_format
# @param s String message to print to terminal and gets user input
# @returns in String whatever the user typed
def get_input(s=""):
    set_format(formats["SYS"])
    return input(s + "\t\u2192 ").strip()


# Simple function that formats a float to a string
# @param number Float the number to be formatted
# @param max_decimals Int the max decimals to include, defaulting to unlimited
# @param min_decimals Int the min decimals to use, defaulting to 0
# @returns formatted String the formatted number as a string
def format_number(number, max_decimals = -1, min_decimals = 0, force_decimals = False):
    formatted = str(number)

    # if -1 then we want all decimals, don't do anything to the formatted value yet
    # if 0 then we don't want any decimals, so thus we can return the int...
    if max_decimals >= 0:
        # simple rounding, returning string of an int
        formatted = str(round(number, ndigits = max_decimals))

    # we do this so that 0.551 won't be stripped to 551 in the next step
    formatted = "_" + formatted
    # This will strip any zeros on either side, and then the '.' if it is now on the end, and then kill the '_'
    formatted = formatted.rstrip("0").rstrip(".").lstrip("_")

    index = formatted.find(".")
    length = len(formatted)
    decimals = length - index - 1
    if index == -1:  # if there is no '.' then add .0 with min_decimals 0 if forced, otherwise return formatted string
        if force_decimals:
            formatted += "."
            while min_decimals > 0:
                formatted += "0"
                min_decimals -= 1
        return formatted
    else:
        # if there are enough or more decimals, don't do anything to the string
        if decimals >= min_decimals:
            return formatted
        else:  # otherwise add 0 until we have enough
            i = min_decimals - decimals
            while i > 0:
                formatted += "0"
                i -= 1

    return formatted


# Dynamically adds \t to put line1 and 2 indented in the same column
# @param line1_first String first part of line 1
# @param line2_first String first part of line 2
# @param line1_indented String second part of line 1, to be in second column
# @param line2_indented String second part of line 2
# @returns formatted String the formatted number as a string
def align_texts(line1_first, line2_first, line1_indented, line2_indented):
    # need these to be the same length
    # test and correct length of lines
    len1 = int(len(line1_first)/4)
    len2 = int(len(line2_first)/4)
    if len1 == len2:
        pass
    elif len1 > len2:
        how_many = (len1 - len2)/4
        while how_many > 0:
            how_many -= 1
            line2_first += "\t"
    else:
        how_many = (len2 - len1)/4
        while how_many > 0:
            how_many -= 1
            line1_first += "\t"

    line1 = line1_first + line1_indented
    line2 = line2_first + line2_indented
    return line1, line2


print(format_number("15656"))

# square
num = float(get_input("What is the length of a side of the square"))
print("The area of the square is: %s\n" % format_number(num*num, max_decimals=2))

# rectangle
num1 = float(get_input("What is the length of the rectangle"))
num2 = float(get_input("What is the width of the rectangle"))
print("The area of the rectangle is: %s\n" % format_number(num1*num2, max_decimals=2))

# circle
r = float(get_input("What is the radius of the circle"))
print("The area of the circle is: %s\n" % format_number(r*r * math.pi, max_decimals=2))

# many shapes:
num = float(get_input("What is the length of a side/circle"))
print("The area of a square of length %d is: %s\n" % (num, format_number(num*num, max_decimals=2)))
print("The area of a circle of radius %d is: %s\n" % (num, format_number(math.pi * num*num, max_decimals=2)))
print("The volume of a cube of length %d is: %s\n" % (num, format_number(num ** 3, max_decimals=2)))
print("The area of a sphere of radius %d is: %s\n" % (num, format_number(4 / 3 * math.pi * num ** 3, max_decimals=2)))
