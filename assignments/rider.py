# Group Assignment 6 -  tells if person(s) cand ride a ride

# --- Imports from my utils ----

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


# -- start actual code
rideable = False

p1_age = int(get_input("How old is the first rider?"))
if 12 <= p1_age < 18:
    if "yes" in get_input("Do they have a golden passport? (yes/no)").lower():
        p1_age = 18

p1_height = int(get_input("How tall is this rider?"))
multiple = "yes" in get_input("Is there a second rider? (yes/no)").lower()
p2_age = 0
p2_height = 36
if multiple:
    p2_age = int(get_input("How old is the second rider?"))
    if 12 <= p2_age < 18:
        if "yes" in get_input("Do they have a golden passport? (yes/no)").lower():
            p2_age = 18

    p2_height = int(get_input("How tall is this rider?"))
    rideable = (p1_age >= 18 or p2_age >= 18) or (p1_age >= p2_age >= 12 and p1_height >= p2_height >= 52) or \
               (abs(p1_age - p2_age) >= 2 and min(p1_age, p2_age) >= 14)
else:
    rideable = p1_age >= 18 and p1_height >= 62

rideable = p1_height >= 36 and p2_height >= 36 and rideable
if rideable: print("You may ride. Please be safe and have fun!")
else: print("Sorry, you may not ride.")

