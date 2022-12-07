# Imported frequently used function
from time import sleep
# Standard delay for slow_type
from sys import stdout
# Used to format phone number
import re

st_delay = .7


# Dictionary holding useful format variables.
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
    "white": "0;97;48",
    "white_underline": "4;97;48"
}

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


story = """The other day, I was really in trouble. It all started when I saw a very 
[adjective] [animal] [verb] down the hallway. "[exclamation]!" I yelled. But all 
I could think to do was to [verb] over and over. Miraculously, 
that caused it to stop, but not before it tried to [verb] 
right in front of my family.
My dad told me to to [verb] to get it to calm down and then clean the mess up with a [noun]. No did he say this, when 
[person] came [verb_ing] into the hallway. Upon seeing the new arrival, the [var_animals0] [verb] over to [var_people0]. 
[var_people0] [verb] and the [var_animals0] sat down. "[exclamation]!" I proclaimed in relief. I will always be 
[emotion] that things didn't go worse."""

# I figured out why the warning shows up... it thinks that i'm trying to close the group, instead of look for ']'
story_parts = re.split("(\[\S[^\]]*\])", story)

print(story_parts)

story_stitched = ""

inputs = {
    "verbs": [],
    "nouns": [],
    "people": [],
    "animals": [],
    "exclamations": [],
    "adjectives": [],
    "verb_ings": [],
    "emotions": []
}

current_part = 0

for part in story_parts:

    # remove all new lines placed in the starter text
    """if "\n" in part:
        part = part.replace("\n", "")
    """

    # get and replace words
    if "[" in part:
        if part == "[verb]":
            part = get_input("Verb: ").lower()
            inputs["verbs"].append(part)
        elif part == "[verb_ing]":
            part = get_input("Verb ending in -ing: ").lower()
            inputs["verb_ings"].append(part)
        elif part == "[adjective]":
            part = get_input("Adjective: ").lower()
            inputs["adjectives"].append(part)
        elif part == "[exclamation]":
            part = get_input("Exclamation").capitalize()
            inputs["exclamations"].append(part)
        elif part == "[noun]":
            part = get_input("Noun: ").lower()
            inputs["nouns"].append(part)
        elif part == "[person]":
            part = get_input("Person: ").capitalize()
            inputs["people"].append(part)
        elif part == "[animal]":
            part = get_input("Animal: ").lower()
            inputs["animals"].append(part)
        elif part == "[emotion]":
            part = get_input("Emotion: ").lower()
            inputs["emotions"].append(part)
        elif "var_" in part:
            part = inputs[part[5:-2]][int(part[-2:-1])]
        else:
            print("ERROR: UNKNOWN PART: " + part)

    story_stitched += part
    current_part += 1


print(story_stitched)
