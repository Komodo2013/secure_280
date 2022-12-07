# Imported frequently used function
from time import sleep
# Standard delay for slow_type
from sys import stdout
# Used to format phone number
import re

st_delay = .7

questions = (
    "name_first",
    "name_last",
    "email",
    "phone",
    "job_title",
    "id",
    "hair",
    "eyes",
    "month",
    "training"
)

questions_text = {
    "name_first": "First name",
    "name_last": "Last name",
    "email": "Email address",
    "phone": "Phone number",
    "job_title": "Current job title",
    "id": "ID number",
    "hair": "Hair color",
    "eyes": "Eye color",
    "month": "Starting month",
    "training": "Have you completed advanced training? Y/N"
}

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
# Below are functions I used last week


# Simple function that formats future text a certain way
# @param format String the text format to be used defined as "int;int;int"
def set_format(style_type):
    print("\x1b[%sm" % style_type, end="")


# Slowly prints string s at fixed speed
# @param s String message to be printed to terminal
# @param delay Float number of seconds to sleep between char
def slow_print(s, delay=st_delay, new_line=True):
    for char in s:
        stdout.write(char)
        stdout.flush()
        sleep(delay)
    if new_line: print("")  # Print new line unless otherwise stated


# Wrapper of print and set_format
# @param s String message to print to terminal and gets user input
# @returns in String whatever the user typed
def get_input(s=""):
    set_format(formats["SYS"])
    return input(s + "\t\u2192 ").strip()


# Used to store answers
class Person:
    answers = {
        "name_first": "",
        "name_last": "",
        "email": "",
        "phone": "",
        "job_title": "",
        "id": "",
        "hair": "",
        "eyes": "",
        "month": "",
        "training": ""
    }


user = Person()

set_format(formats["SYS"])

print("Preparing to create new ID card", end="")
slow_print("...")
print("\nPlease enter the following information:\n")

# start spam of info
for q in questions:
    user.answers[q] = get_input(questions_text[q])

print("\nPreparing ID card", end="")

# formatting user answers
# really wish there was a switch statement in python
for k, v in user.answers.items():
    if k == "name_first" or k == "job_title":
        user.answers[k] = v.title()  # just in case someone has 2 first names/ last names
    elif k == "name_last":
        user.answers[k] = v.upper()
    elif k == "email":
        user.answers[k] = v.lower()
    elif k == "phone":
        user.answers[k] = format_phone(v)
    elif k == "id":
        pass  # we don't need to do anything to id num
    else:
        user.answers[k] = v.title()  # everything else can be capitalized

print(".", end="")  # display a loading dot

top_section = ""
bar_line = ""
i = 0
while i < 30:  # lazy - or should I say easy to change
    bar_line += "-"
    i += 1

top_section += bar_line + "\n"

line = "%s, %s\n" % (user.answers["name_first"], user.answers["name_last"])
top_section += line

line = "%s\n" % user.answers["job_title"]
top_section += line

print(".", end="")  # display a loading dot

line = "ID: \x1b[%sm%s \n\n\x1b[%sm" % (formats["green"], user.answers["id"], formats["SYS"])
top_section += line


line = "%s\n" % user.answers["email"]
top_section += line

line = "%s\n\n" % user.answers["phone"]
top_section += line

print(".", end="")  # display a loading dot

bottom_section = ""

# need these to be the same length
line1 = "Hair: \x1b[%sm%s\t\t" % (formats["green"], user.answers["hair"])
line2 = "Month: \x1b[%sm%s\t\t" % (formats["green"], user.answers["month"])

# test and correct length of lines
# hahaha... So I did this in a way harder method than {variable:int}.... oh well
len1 = int(len(line1)/4)
len2 = int(len(line2)/4)
if len1 == len2:
    pass
elif len1 > len2:
    how_many = (len1 - len2)/4
    while how_many > 0:
        how_many -= 1
        len2 += "\t"
else:
    how_many = (len2 - len1)/4
    while how_many > 0:
        how_many -= 1
        len1 += "\t"

line1 += "\x1b[%smEyes: \x1b[%sm%s\n\x1b[%sm" % (formats["SYS"], formats["green"], user.answers["eyes"], formats["SYS"])

# make the n red if they didn't attend training
form = formats["green"]
if user.answers["training"] == "N":
    form = formats["red"]

line2 += "\x1b[%smTraining: \x1b[%sm%s\n\x1b[%sm" % (formats["SYS"], form, user.answers["training"], formats["SYS"])

print(".", end="")  # display a loading dot

id_card = top_section + line1 + line2 + bar_line

print(".\n")  # display a loading dot
print(id_card)

# TODO: check for valid email/phone number
