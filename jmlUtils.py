# A collection of semi-useful programs which I've collected to make things easier on myself
import random
import re
import sys
import time


# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
formats = {
    "SYS": "\x1b[0;97;48m",
    "TOBAR": "\x1b[0m",
    "PLAYER": "\x1b[0m",
    "WARNING": "\x1b[0;93;48m",
    "ERROR": "\x1b[0;91;48m",
    "INFO": "\x1b[0;96;48m",
    "black": "\x1b[0;97;40m",
    "grey": "\x1b[0;37;48m",
    "red": "\x1b[0;31;48m",
    "green": "\x1b[0;92;48m",
    "yellow": "\x1b[0;33;48m",
    "blue": "\x1b[0;94;48m",
    "purple": "\x1b[0;95;48m",
    "cyan": "\x1b[0;36;48m",
    "white": "\x1b[0;97;48m"
}
# Light version of the above
# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
form = {
    "g": "\x1b[0;92;48m",
    "w": "\x1b[0;97;48m",
    "y": "\x1b[0;93;48m",
    "r": "\x1b[0;91;48m",
    "grey": "\x1b[0;37;48m",
}


# Simple function that formats a phone number
# @param raw_phone String the text to parse into a phone-number format
def format_phone(raw_phone):
    phone = re.sub('[^0-9]+', '', raw_phone)
    # I don't know why there is a soft-warning here.... w3schools expressively declares that \d is a valid token
    separated_number = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1 ", "%d" % int(phone[:-1])) + phone[-1]
    divided = separated_number.split(" ")
    if len(divided) == 4:
        return "+" + divided[0] + " (" + divided[1] + ") " + divided[2] + "-" + divided[3]
    elif len(divided) == 3:
        return "(" + divided[0] + ") " + divided[1] + "-" + divided[2]
    elif len(divided) == 2:
        return divided[0] + "-" + divided[1]
    else:
        return divided[0]


def slow_type(t, typing_speed = 50):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random() * 10.0 / typing_speed)
    print('')


def print_slow(s, delay = 0.05):
    for letter in s:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(delay)
    print('')

# Slowly prints string s at fixed speed
# @param s String message to be printed to terminal
# @param delay Float number of seconds to sleep between char
def slow_print(s, delay = 0.7, new_line = True):
    for char in s:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    if new_line: print("")  # Print new line unless otherwise stated


# Wrapper of print and set_format
# @param s String message to print to terminal and gets user input
# @returns in String whatever the user typed
def get_input(s=""):
    return input(formats["SYS"] + s + "\t\u2192 ").strip()


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
