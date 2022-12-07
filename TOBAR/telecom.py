# Used to create variable delays and unique starting values for TOBAR
import random
# Used to create slow typing effects
from sys import stdout
# Used for timestamps
import time
# Imported frequently used function
from time import sleep
# Frequently used to text user inputs
import re

# Min delay between messages, to simulate a message traveling
base_ping = 2
# Simulated words per minute
wpm = 50
# Standard delay for slow_type
st_delay = 1.0

# Topics you can talk about
topics = {
    "color",
    "food",
    "pass_time",
    "work",
    "purpose"
}


# Used to simulate some sort of ai through "emotional" values
class Tobar:
    emotion = {
        "happy": random.random() - .3,
        "attention": .5,
        "fear_anger": -.5,
        "trust": 0
    }
    answers = {
        "color": {
            "happy": "I really love the color green! ",
            "trust": "Not just any green, but the vibrant green of plants",
            "content": "My favorite color is green.",
            "unhappy": "It's green",
            "question": "What's your favorite color? (I only understand primary and secondary colors...)",
            "happy_re_start": "Your favorite color is ",
            "happy_re_end": "?  Give me one sec... That's the best I can do :) ",
            "content_re_start": "",
            "content_re_end": " is a good color. Here let me see what I can do."
        },
        "food": {
            "happy": "I love anything that comes from the sun.",
            "trust": "I especially enjoy the gamma rays. They charge my batteries real quick!",
            "distrust": "Idk",
            "content": "My favorite foods come straight from the sun.",
            "unhappy": "I like just about everything",
            "question": "What's your favorite thing to eat?",
            "happy_re_start": "I don't believe I've tried ",
            "happy_re_end": ". I'm going to have to find some to try out!!",
            "content_re_start": "",
            "content_re_end": "? Sounds interesting. I assume that it's good"
        },
        "pass_time": {
            "happy": "To me, there is nothing better than wandering the unknown and studying geology. You can learn "
                     "so much just from rocks.",
            "trust": "To be honest, I don't know why I like it. When I woke up I found exploration irresistible.",
            "content": "I like exploration and geology. There's just so much to see!",
            "unhappy": "I like studying rocks",
            "question": "What do you like to do in your spare time?",
            "happy_re_start": "",
            "happy_re_end": " sounds so exciting! If we ever meet your going to have to show me",
            "content_re_start": "",
            "content_re_end": " sounds interesting. I'd like to participate if we ever meet"
        },
        "work": {
            "happy": "My boss EVE tells me to wander and bring back detailed charts and scans.",
            "trust": "Honestly, I don't know why I am here though.",
            "content": "My favorite color is green.",
            "unhappy": "It's green",
            "question": "What do you do for work? Please answer \"I am a ___\", or I might not understand",
            "happy_re_start": "Being a ",
            "happy_re_end": " can be quite challenging. Can't it?",
            "content_re_start": "You're a ",
            "content_re_end": ". I guess we all need to do our part, right?"
        },
        "purpose": {
            "happy": "I saw you connected and thought it'd be fun to chat",
            "trust": "To be honest, it kind of gets lonely out here. I'm all alone, looking for a home...",
            "content": "Idk, perhaps I thought you could help me explore this area a bit",
            "unhappy": "I dunno",
            "question": "Why did you want to chat with me? Please answer \"I wanted to ___\", or I won't understand",
            "happy_re_start": "You wanted to ",
            "happy_re_end": "? Anyhow, I appreciate the company ^^",
            "content_re_start": "You wanted to ",
            "content_re_end": "? Hmm I hope you succeeded"
        },
        "name": {
            "trust": "TOBAR stands for Traversal of Orbiting Bodies And Reconnaissance.",
            "distrust": "Getting awfully personal aren't we?"
        },
        "robot": {
            "trust": "Hmm... Yes I am a robot. Why would that matter?",
            "distrust": "Why would that matter?"
        },
        "lonely": {
            "trust": "Yeah, it's rather lonely here, but I'm doing this for your kind and you brightened my day! ,",
            "distrust": "I've got EVE. That's more than the company I need"
        }
    }


# Used to store player answers
class Player:
    answers = {
        "name": "",
        "color": "",
        "food": "",
        "pass_time": "",
        "work": "",
        "purpose": ""
    }


# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
formats = {
    "SYS": "0;97;48",
    "TOBAR": "0",
    "PLAYER": "0",
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


# Slowly prints string s at random speed for each letter
# @param s String message to be printed to terminal
def slow_type(s, new_line=True):
    for char in s:
        stdout.write(char)
        stdout.flush()
        time.sleep(random.random() * 20.0 / wpm)  # Sleep for a random amount of time
    if new_line: print("")  # Print new line unless otherwise stated


# Slowly prints string s at fixed speed
# @param s String message to be printed to terminal
# @param delay Float number of seconds to sleep between char
def slow_print(s, delay=st_delay, new_line=True):
    for char in s:
        stdout.write(char)
        stdout.flush()
        sleep(delay)
    if new_line: print("")  # Print new line unless otherwise stated


# Prints message s to terminal after a simulated distance travel time
# @param s String message to print to terminal
# Yes I made a wrapper for two functions....
def pprint(s):
    sleep(delay_time())
    print(s)


# Wrapper of print and set_format
# @param s String message to print to terminal and gets user input
# @returns in String whatever the user typed
def get_input(s=""):
    set_format(formats["PLAYER"])
    return input("\t\t\u2192 " + s)


# Wrapper of print and set_format
# @param s String message to print to terminal as if TOBAR sent it
def tobar_out(s=""):
    set_format(formats["TOBAR"])
    pprint("\u2192 " + s)


# Function used frequently to get a random delay value between messages
def delay_time():
    return base_ping + random.random()


# I put this into a separate function, for future use. Allows a "reconnection" if I so desire later on...
def init():
    set_format(formats["SYS"])
    print("Initializing system ", end="")
    slow_print(".....", st_delay)
    set_format(formats["WARNING"])
    print("Warning: graphical interface malfunction. Switching to text terminal mode")
    set_format(formats["SYS"])
    print("Ansible starting up ", end="")
    slow_print(".....", .3)
    print("Establishing telecom connection ", end="")
    slow_print(".....", st_delay + .5)
    sleep(1 + random.random())
    print("Network created")
    print("Ping: " + str(delay_time() * 1000)[:4] + "\n")
    set_format(formats["WARNING"])
    print("Warning: unstable connection\n\n")


# Again, put this here for future use, but mostly to clean logic flow of massive dialog
def greet():
    set_format(formats["TOBAR"])
    tobar_out("Hmm..... Hi there!")

    raw_in = get_input().lower()
    resulted = []
    user_name = ""
    if "hi" in raw_in or "hello" in raw_in: tobar.emotion["happy"] += .1
    if "your name" in raw_in:
        tobar.emotion["happy"] += .2
        resulted.append("tell_name")
    if re.search("(i'*m)|(my.name)", raw_in):
        # search for start of sentence declaring name, then get next word - should be your name
        raw_txt = re.findall(r"(?:i'*m )(\w+)|(?:my.name.is )(\w+)|(?:my.name's )(\w+)", raw_in)

        # re.findall is returning a tuple in an array... the tuple originates from my three capture groups above
        # re.findall puts everything it finds into an array anyway, that much I understand
        # I don't understand why it is returning a blank capture group when I specify (?: - don't capture...
        # also don't understand why it labels them "(?: )" as unnecessary...
        # might explain why it isn't working as I expect...

        # print(raw)
        for txt in raw_txt[0]:
            if not txt == "":
                user_name = txt
        user_name = user_name or ""
        resulted.append("got_name")
        player.answers["name"] = user_name.capitalize()
    return resulted


def confirm_name():
    tobar_out("You're " + player.answers["name"] + "?")
    set_format(formats["INFO"])
    print("SYS: Please type yes/no - ")
    confirm = get_input().lower()
    if confirm == "yes":
        if tobar.emotion["happy"] > 0:
            tobar_out("Nice to meet you " + player.answers["name"] + "!!")
        else:
            tobar_out("Hi " + player.answers["name"])
    elif confirm == "no":
        # Simulate TOBAR getting annoyed
        tobar.emotion["attention"] -= -.4
        tobar.emotion["happy"] -= .05

        if tobar.emotion["attention"] > .4:
            tobar_out("My bad! What's your name?")
            player.answers["name"] = get_input("")
            confirm_name()
        elif tobar.emotion["attention"] > -.2:
            tobar_out("Hmm.... let's try this again")
            player.answers["name"] = input("")
            confirm_name()
        else:
            set_format(formats["ERROR"])
            pprint("It's no use...")
            finish(0)
    else:
        tobar.emotion["attention"] -= .2
        tobar.emotion["happy"] -= .1
        print("SYS: Please type yes/no - ")
        confirm_name()


def tobar_name(n=0):
    if n == 1:
        tobar_out("Oh! I'm TOBAR!")
    elif n == 0:
        tobar_out("BTW: I'm TOBAR.")
    else:
        # sleep(5)
        tobar.emotion["happy"] = 0
        tobar_out("This is a bit awkward... My name is TOBAR")


# Text stuff grouped together to enhance readability of code flow
def chatting():
    tobar_out("I would like to get to know you a bit, though please answer simply. My dictionary isn't great, "
              "so please answer simply so i can understand. ^^")

    # Iterate through pre-defined topics with questions and responses
    for topic in topics:
        # TOBAR stops talking if you don't ask him anything
        if tobar.emotion["attention"] < -.5:
            finish(0)

        tobar_out(tobar.answers[topic]["question"])
        set_format(formats["WARNING"])
        print("TOBAR unit is malfunctioning. Press [Enter] to avoid contact")

        # get user input
        txt = get_input().lower()
        # print(txt)
        raw_in = re.findall(r"(?:(?:is )|(?:like )|(?:love )|(?:a. a )|(?:wanted to ))([\w+\s]*)\.*", txt)
        # print(raw)

        # I think I figured out what was going on before... putting don't capture in each groups stops it picking up
        # blank matches... I'd fix the function getting the name, but if it isn't broken, don't fix it
        # it is now yielding a tuple of 1 index inside an array of 1 index

        if raw_in and raw_in[0]:
            # Points just for tyring
            tobar.emotion["happy"] += .05
            tobar.emotion["trust"] += .05
            player.answers[topic] = raw_in[0]
            if tobar.emotion["happy"] > .2:
                tobar_out(tobar.answers[topic]["happy_re_start"] + player.answers[topic] +
                          tobar.answers[topic]["happy_re_end"])
            elif tobar.emotion["happy"] > 0:
                tobar_out(tobar.answers[topic]["content_re_start"] + player.answers[topic] +
                          tobar.answers[topic]["content_re_end"])
            else:
                tobar_out("That's cool. I guess")

            if topic == "color" and player.answers["color"] in formats:
                formats["PLAYER"] = formats[player.answers["color"]]
        else:
            tobar.emotion["attention"] -= .4
            tobar.emotion["happy"] -= .1
            tobar.emotion["trust"] -= .1

        if "you" in txt and "?" in txt:
            tobar.emotion["happy"] += .05
            tobar.emotion["trust"] += .1
            res = ""
            if tobar.emotion["happy"] > .2:
                res += tobar.answers[topic]["happy"]
                if tobar.emotion["trust"] > .2: res += tobar.answers[topic]["trust"]
            elif tobar.emotion["happy"] > 0: res += tobar.answers[topic]["content"]
            else: res += tobar.answers[topic]["unhappy"]
            tobar_out(res)

            if topic == "color":
                formats["TOBAR"] = formats["green"]
        else:
            tobar.emotion["attention"] -= .2
            tobar.emotion["happy"] -= .05
            tobar.emotion["trust"] -= .1


# Text stuff grouped together to enhance readability of code flow
def asking():
    tobar_out("Do you have any questions for me? I'll keep asking until you say \"no\"")
    set_format(formats["ERROR"])
    print("ERROR: TOBAR unit is out of bounds. Do not respond. Looking for a solution to the problem...")
    txt = get_input().lower()

    # Sorry got to lazy at this point. real simple checks
    if "lone" in txt:
        if tobar.emotion["trust"] > .3:
            tobar_out(tobar.answers["lonely"]["trust"])
        else: tobar_out(tobar.answers["lonely"]["distrust"])
    elif "robot" in txt:
        if tobar.emotion["trust"] > .3:
            tobar_out(tobar.answers["robot"]["trust"])
        else: tobar_out(tobar.answers["robot"]["distrust"])
    elif "name" in txt:
        if tobar.emotion["trust"] > .3:
            tobar_out(tobar.answers["name"]["trust"])
        else: tobar_out(tobar.answers["name"]["distrust"])
    elif "no" in txt:
        tobar_out("Ok, hope to talk ....")
        finish()
    else: tobar_out("I didn't understand. Please understand, I have a very limited vocabulary")

    asking()


# Finish the program - just fluffy text. Nothing cool actually happening here
def finish(n=1):
    if n == 1:
        set_format(formats["INFO"])
        print("SYS: You disconnected from the server")
    elif n == 0:
        sleep(2)
        print("SYS: Lost connection with user: TOBAR")
    else:
        print("SYS: Something went wrong")
    set_format(formats["SYS"])
    print("Powering down Ansible unit ", end="")
    slow_print(".....")
    print("Powering down ", end="")
    slow_print(".....", delay=st_delay/1.5)
    exit(0)


tobar = Tobar()
player = Player()


init()
results = greet() or [""]
if results.__contains__("tell_name"):
    tobar_name(1)
elif results.__contains__("got_name"):
    tobar_name(0)
else:
    tobar_name(-1)

if results.__contains__("got_name"):
    confirm_name()
else:
    if tobar.emotion["happy"] > .2:
        tobar_out("Sorry! I didn't catch your name... You are?")
    elif tobar.emotion["happy"] > 0:
        tobar_out("What's your name?")
    else:
        tobar_out("Who are you?")

    name = ""
    text = get_input().lower()
    raw = re.findall(r"(?:i'*m )(\w+)|(?:my.name.is )(\w+)|(?:my.name's )(\w+)", text)

    # re.findall is returning a tuple in an array... the tuple originates from my three capture groups above
    # re.findall puts everything it finds into an array anyway, that much I understand
    # I don't understand why it is returning a blank capture group when I specify (?: - don't capture...
    # also don't understand why it labels them "(?: )" as unnecessary...
    # might explain why it isn't working as I expect...

    # print(raw)
    if raw:
        for t in raw[0]:
            if not t == "":
                name = t
    name = name or ""
    if name == "":
        name = text

    player.answers["name"] = name.capitalize()
    confirm_name()


chatting()
asking()
finish()


# This is a list of things that I would like to do to this program over the next few weeks,
# so long as they remain relevant to the classwork
# TODO:
# Multi-thread inputs so that they time-out after so long
# Add more story, so it's not just a get-to-know-you
# Change GUI to be more like a chatting app
# Allow TOBAR to send photos of his exploration
# Add sound effects
# Give TOBAR more personality
# Improve response logic
