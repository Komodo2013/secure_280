# Used to create variable delays and unique starting values for TOBAR
import random
# Used to create slow typing effects
import sys
# Used for timestamps
import time
# Imported frequently used function
from time import sleep

# Min delay between messages, to simulate a message traveling
base_ping = 2
# Standard delay for slow_type
st_delay = 1.0


class Cell:
    def __init__(self, entry_text, available_actions):
        self.entryText = entry_text
        self.availableActions = available_actions
        self.usedActions = []
        self.visited = False


# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
formats = {
    "SYS": "\x1b[0;97;48m",
    "TOBAR": "\x1b[0;32;48m",
    "PLAYER": "\x1b[0m",
    "WARNING": "\x1b[0;93;48m",
    "ERROR": "\x1b[0;91;48m",
    "INFO": "\x1b[0;96;48m",
    "EMPHASIS": "\x1b[0;93;48m",
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


# Holds data of world interaction objects
world = {
    # Recharge Rate
    "recharge": 1,
    # Capacitor recharge
    "capacitor": 20,
    "city_visited": False
}


# Holds data particular to TOBAR (the main character)
tobar = {
    # list holding TOBAR's current coordinates - changed to 2 variable cause its faster to access
    "x": 1,
    "y": 1,
    # TOBAR's hp
    "hp": 100.0,
    # TOBAR's available energy
    "energy": 100.0,
    "first": "",
    "death_counter": 0
}


# Holds available actions, a run msg, and energy costs
actions = {
    # scan - detect nearby items of interest (structures/terrain/energy signals costs energy
    "scan": {
        "cost": 7,
        "run": "Scanning nearby structures.... hang on..."
    },
    # look - run automatically each time you enter an area
    "look": {
        "cost": 0,
        "run": ""
    },
    # laser - takes energy to shoot at something
    "laser": {
        "cost": 15,
        "run": "Charging... ZAAPPP"
    },
    # go direction - moves tobar that way (n, s, e, w, left, straight, right, back
    "go": {
        "cost": 2,
        "run": "Alright, I'll go until I find something interesting..."
    },
    # run - go fast away (opposite direction you came)
    "run": {
        "cost": 4,
        "run": "AAAAAAHHHH"
    },
    # investigate - rummage through stuff
}


terrain = [
    [
        Cell("I'm at the base of a tall mountain..", {
            "scan": f"I am detecting {formats['EMPHASIS']}E.V.E.'s signal{formats['TOBAR']}on the other side of the "
                    f"mountain. Unfortunately, it's too steep to climb. I'll have to look for a way "
                    f"{formats['EMPHASIS']}through{formats['TOBAR']} it.",
            "look": "The rocky terrain seems impassable, but I found a cave entrance..."
        }),
        Cell(f"I seem to be in a field of hills. A river extends from the mountain eastward.", {
            "scan": f"A mountain lies due west of here. There seems to be {formats['EMPHASIS']}E.V.E.'s faint signal"
                    f"{formats['TOBAR']} coming beyond the mountain. A forest lies to the east.",
            "look": f"There isn't much around, just a river running eastward... I should find "
                    f"{formats['EMPHASIS']}E.V.E.{formats['TOBAR']} and get"
                    " out of here. This planet seems hostile..."
        }),
        Cell("There appears to be a weird forest growing in this area.", {
            "scan": f"I can detect {formats['EMPHASIS']}city ruins {formats['TOBAR']}north of here. My scanner "
                    f"{formats['EMPHASIS']}seems to be jammed{formats['TOBAR']} scanning southward.",
            "look": "A river runs eastward. I won't cross that. A dense fog seems to be settling on the forest."
        })
    ],
    [
        Cell("I'm in a vast and empty wasteland with very rocky terrain westward.", {
            "scan": f"I am detecting a {formats['EMPHASIS']}faint signal {formats['TOBAR']}is southwest of here. "
                    f"My {formats['EMPHASIS']}landing pod{formats['TOBAR']} seems to be northeast of here."
                    f"A mountain lies south of here.",
            "look": "The rocky terrain seems impassable."
        }),
        Cell(f"I seem to be in the middle of nowhere. The terrain is rough yet traversable.", {
            "scan": f"A mountain lies south-west of here. There seems to be {formats['EMPHASIS']}large "
                    f"craters{formats['TOBAR']} and possibly {formats['EMPHASIS']}buildings{formats['TOBAR']}"
                    f" to the east. I detect my {formats['EMPHASIS']}landing pod {formats['TOBAR']}to the north.",
            "look": "Its an empty rocky wasteland... Nothing interesting here"
        }),
        Cell("I see a bunch of craters with what appear to be building remains. Perhaps I could look around?", {
            "scan": f"I detect my {formats['EMPHASIS']}landing pod {formats['TOBAR']}is north west of here. A faint "
                    f"{formats['EMPHASIS']}energy signal is detected nearby{formats['TOBAR']} perhaps I could find it.",
            "look": "Alright, I'll look around the ruins."
        })
    ],
    [
        Cell("All I see here is a big ravine.", {
            "scan": f"I detect my {formats['EMPHASIS']}landing pod {formats['TOBAR']}is east of here. "
                    "There's a mountain to the south.",
            "look": "Like I said big ravine. There is no way down it"
        }),
        Cell(f"There's a big ravine slightly north. I found my {formats['EMPHASIS']}landing pod{formats['TOBAR']}. "
             "Unfortunately it crashed.", {
                 "scan": f"A mountain lies south-west of here. There seems to be {formats['EMPHASIS']}large "
                         f"craters{formats['TOBAR']} and possibly {formats['EMPHASIS']} buildings {formats['TOBAR']}"
                         " to the east",
                 "look": "My escape pod is definitely busted. There is no way I'll be able to get it running again."
                         " Looks like something hit it..."
             }),
        Cell("I see a bunch of craters, and the ravine continues north", {
            "scan": f"I detect my {formats['EMPHASIS']}landing pod {formats['TOBAR']}is west of here. The craters "
                    f"consist of {formats['EMPHASIS']}ionized mineral and organic remains{formats['TOBAR']}."
                    f" There are {formats['EMPHASIS']}city ruins{formats['TOBAR']} south.",
            "look": "The craters are large and rugged, rendering them non-traversable"
        })
    ]
]


# Slowly prints a string with configurable delay
# @param s String the string to slowly print to screen
# @param delay Float optional input for aprox delay in seconds between each character
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
# @returns in String whatever the user typed after being lowered
def get_input(s=""):
    return input(formats["SYS"] + s + "\t\u2192 ").strip().lower()


# Wrapper of print and set_format
# @param s String message to print to terminal as if TOBAR sent it
def tobar_out(s=""):
    sleep(delay_time())
    print(formats["TOBAR"] + "\u2192 " + s)


# Wrapper to get a formatted string with energy colored by number
# @returns String message formatted with color
def get_energy_text():
    if tobar["energy"] > 50:
        form = formats["blue"]
    elif tobar["energy"] > 25:
        form = formats["yellow"]
    else:
        form = formats["red"]
    return f"Energy: {form}{tobar['energy']:.1f}\t\t {formats['TOBAR']}"


# Wrapper to get a formatted string with hp colored by number
# @returns String message formatted with color
def get_hp_text():
    if tobar["hp"] > 50:
        form = formats["blue"]
    elif tobar["hp"] > 25:
        form = formats["yellow"]
    else:
        form = formats["red"]
    return f"Hp: {form}{tobar['hp']:.0f}\t\t {formats['TOBAR']}"


# Function used frequently to get a random delay value between messages
def delay_time():
    return base_ping + random.random()


# I put this into a separate function, for future use, like now. Allows a "reconnection" if I so desire later on...
def init():
    print(formats["SYS"] + "Initializing system ", end="")
    slow_print(".....", st_delay)
    print(formats["WARNING"] + "Warning: graphical interface malfunction. Switching to text terminal mode")
    print(formats["SYS"] + "Ansible starting up ", end="")
    slow_print(".....", .3)
    print("Establishing telecom connection ", end="")
    slow_print(".....", st_delay + .5)
    sleep(1 + random.random())
    print("Network created")
    print("Ping: " + str(delay_time() * 1000)[:4])
    print(formats["WARNING"] + "Warning: connection unstable\n\n" + formats["SYS"])
    sleep(1 + random.random())
    print(formats["TOBAR"] + "Hello again! I'm TOBAR. Remember me?\nI've run into a bit of a problem.", end="")
    slow_print("..", .3)
    print(f"I've managed to crash-land onto some planet. Please help me escape! ")


# prints out the available actions to terminal
def commands_help():
    print(f"{formats['INFO']}Type '/help' to see this again")
    print(f"'go <direction>' moves TOBAR - accepts north/south/east/west. Costs {actions['go']['cost']} energy")
    print(f"'look' TOBAR will report what it can see. Costs {actions['look']['cost']} energy")
    print(f"'scan' TOBAR will scan the area and give a report. Costs {actions['scan']['cost']} energy")
    # print(f"'laser' TOBAR will shoot its laser. Costs {actions['laser']['cost']} energy")
    # print(f"'run' TOBAR will flee the area at full speed. Costs {actions['run']['cost']} energy\n")


# wrapper of the if statement testing if tobar is out of energy or hit points
def is_dead():
    return tobar["energy"] <= 0 or tobar["hp"] <= 0


# Got this poem from a creative commons site, but still giving him credit
# This poem contains the clues neccessary to beat the tunnel portion
# For person/educational use only
def print_poem():
    tobar_out(f"""So Many Directions by Robert Longley\n
So many directions\nWhich way will you go\nwill you sit and watch the day\nor is it time to grow\n
There is {formats["EMPHASIS"]}no one right answer{formats["TOBAR"]}\nor path that you should take
but it is about intention\nin decisions that you make\n
will you {formats["EMPHASIS"]}find beauty\nwithout a change of view{formats["TOBAR"]}
or maybe a {formats["EMPHASIS"]}change of direction{formats["TOBAR"]}\nis just what you must do\n
{formats["EMPHASIS"]}There's many ways to get there{formats["TOBAR"]}\nit's just that you must start
you know where you are going\ndeep within our heart""")


# Fluffy text to print at the end, then close the program
def finish():
    print(formats["INFO"] + "TOBAR disconnected from the server.")
    print("Powering down Ansible unit ", end="")
    slow_print(".....")
    print("Powering down ", end="")
    slow_print(".....", delay=st_delay/1.5)
    exit(0)


# part of the story, put here mostly for readability
def explore_tunnel():
    tobar["energy"] -= actions["go"]["cost"]/2
    tobar_out(f"There are strange markings here... It says {formats['EMPHASIS']}'So Many Directions'{formats['TOBAR']}")

    # test to see if we know about the poem
    if world["city_visited"]:
        tobar_out("Wait! That's the name of that poem. There might be clues in it! Let me recall it...")
        print_poem()
    tobar_out(get_energy_text() + "The cave opens up to three paths. Which do I take?")

    # first choice here
    tobar["first"] = get_input("(left/straight/right)")
    if "right" in tobar["first"]:
        tobar_out(get_energy_text() + "Nothing seems out of the ordinary... AHH!")
        tobar["energy"] -= 10
        tobar["hp"] -= 40
        if is_dead(): return True  # testing if he died.. if so end this loop

        sleep(delay_time()*1.5)
        print(f"{formats['INFO']}Lost connection with user: TOBAR")
        sleep(delay_time())  # pretending we lost connection when he was burried
        print(f"{formats['INFO']}Connection reestablished with user: TOBAR")
        tobar_out(get_energy_text() + get_hp_text() + "There was a trap... it dumped a bunch of rocks on me...")
        tobar_out(get_energy_text() + get_hp_text() + "I'm back at the intersection. Which way should I go?")

        # test player input again
        tobar["first"] = get_input("(left/straight/out)")
        # if we want to leave, leave cave and return to terrain dialogs
        if "out" in tobar["first"]:
            tobar["energy"] -= 1
            tobar_out(get_energy_text() + get_hp_text() + "I'm out of here")
            return False

    if "left" in tobar["first"]:
        tobar["energy"] -= 1
        tobar_out(get_energy_text() + "It was a dead end... but a note read: 'right is a trap'")

        # test input again....
        tobar["first"] = get_input("Which way? (straight/right/out)")
        if "right" in tobar["first"]:
            tobar_out(get_energy_text() + "Yeah... not listening.")
            tobar["first"] = get_input("Which way? (straight/out)")
        if "out" in tobar["first"]:
            tobar["energy"] -= 1
            tobar_out(get_energy_text() + "I'm out of here")
            return False

    # continue with story
    if "straight" in tobar["first"]:
        tobar["energy"] -= 1
        tobar_out(get_energy_text() + "A path diverts off to the left. Which do I take?")

        # next choice
        second = get_input("(left/straight)")
        if "left" in second:
            tobar["energy"] -= 1
            tobar_out(get_energy_text() + "It was a dead end...")
            if "out" in get_input("Should I go out or down the straight path? (straight/out)"):
                tobar_out(get_energy_text() + "I'm out of here")
                return False

        # going straight
        tobar["energy"] -= 1
        tobar_out(get_energy_text() + "A path diverts off to the right. Which do I take?")

        # third choice
        choice = get_input("(straight/right)")
        if "right" in choice:
            tobar["energy"] -= 1
            tobar_out(get_energy_text() + "There's sticky string all over the place... Oh dear...")

            # another choice... defend or flee
            answer = get_input("Movement! Shoot or run? (laser/run)")
            if "laser" in answer:
                tobar["energy"] -= actions["laser"]["cost"]
                tobar_out(get_energy_text() + "Charging... ZAAAPP")
                tobar["hp"] -= 35
                if is_dead(): return True  # test if he died again...

                tobar_out(get_energy_text() + get_hp_text() + "Arrg! It hit me! Target acquired.... ZAAAPP!")
                tobar_out(get_energy_text() + "Stupid giant arachnid...thing...")

                # if we want out, then return to terrain dialog
                if "straight" not in get_input("Continue straight or leave? (straight/out)"):
                    tobar_out(get_energy_text() + "I'm out of here")
                    return False
            else:
                tobar["energy"] -= actions["run"]["cost"]
                tobar_out(get_energy_text() + "AAAHHHHH!")
                tobar["hp"] -= 13
                if is_dead(): return True  # test if living
                tobar_out(get_energy_text() + get_hp_text() + "It got me, but not bad. But I'm out of here!")
                return False  # return to terrain dialog

        # If I'm here we are going straight, continue story
        tobar_out(f"The tunnel ends... but there is a room full of the most {formats['EMPHASIS']}beautiful crystals!")
        tobar_out(f"Unfortunately that doesn't get me home... AH! I found a tunnel to the right")
        last = get_input("Should I turn around or take the tunnel to the right? (right/turn around)")

        # right is a no win scenario
        if "right" in last:
            tobar_out(f"This was a terrible mistake... There's a whole bunch of creatures. I'm going to quietly leave")
            tobar_out(f"Great... One's blocking the path...")
            if "laser" in get_input("Fire my laser or run for it? (laser/run)"):
                tobar["energy"] -= actions["laser"]["cost"]
                tobar_out(get_energy_text() + "Charging... ZAAAPP")
                tobar_out(f"Oh that made them mad!")

                # keep shooting until he runs out of energy
                while tobar["energy"] > 0:
                    tobar["energy"] -= actions["laser"]["cost"]/2
                    tobar_out(get_energy_text() + "Charging... ZAAAPP")
                return is_dead()
            else:
                tobar_out(f"It grabbed me! I can't get free....")
                tobar["hp"] = 0
                return is_dead()  # I actually don't do anything with the returned boolean... but it adds readability

        # we turned around
        else:
            tobar_out(f"Hey look! Its another path I didn't see!")
            if "no" in get_input("Should I take it? (yes/no)"):
                # leave the cave
                tobar_out("I was able to make it out safely.")
                return False
            else:
                # take secret path and win
                tobar_out(f"Hey look! Light!")
                tobar_out(f"I exited the tunnel. E.V.E.'s landing pod signal is close! It's right over there in fact!")
                tobar_out(f"Thank you for helping me escape!!")
                print(f"{formats['INFO']}You beat the game with {tobar['death_counter']} deaths.")
                finish()


def explore_city():
    # test if we've been here before and quit if we have
    if world["city_visited"]:
        tobar_out("That place was scary. I'm not going back...")
        return
    world["city_visited"] = True  # you only get 1 shot at this

    tobar_out(get_energy_text() + "Most of the stuff here is in shambles. Some buildings are nothing but foundations..")
    tobar["energy"] -= 0.5
    tobar_out(get_energy_text() + "I've come to the once largest building. A signal is emanating beneath this rock..")
    tobar["energy"] -= 0.5
    tobar_out(get_energy_text() + "I managed to move the rubble... There's a basement! I'll check it out.")
    tobar["energy"] -= 0.1
    tobar_out(get_energy_text() + "The walls seem to be made of a hard, organic crystal. It's dark in here.")
    tobar_out(get_energy_text() + "There's a computer interface here that I can use.")

    # first choice
    if "no" in get_input("Should I connect to it? (yes/no)"):
        tobar_out("You're right... I should just get out of here...")
    else:
        tobar_out(get_energy_text() + "There's a lot of files here... interesting that most I can read.")
        tobar["energy"] += 0.1
        tobar_out(get_energy_text() + "Ah! It appears to be a satellite we sent to space..")
        tobar["energy"] += 0.1
        tobar_out(get_energy_text() + "A certain file is marked as important... a poem called 'So Many Directions'")

        # the biggest piece of the story that we need... this poem
        print_poem()
        tobar["energy"] += 0.1
        tobar_out(get_energy_text() + "Nothing else is interesting on this computer...")

        # second choice
        if "yes" in get_input("Should I drain it's capacitor to recharge my batteries? (yes/no)"):
            tobar["energy"] = min(tobar["energy"] + world["capacitor"], 100.0)
            tobar_out(get_energy_text() + "Very refreshing!")
            tobar_out(get_energy_text() + "Wait... What was that? I thought I saw movement..")

            # third choice
            if "laser" in get_input("Fire laser or run? (laser/run)"):
                tobar_out(get_energy_text() + "Charging laser...")
                tobar["energy"] -= actions["laser"]["cost"]
                if is_dead(): return True  # test if we just died
                tobar_out(get_energy_text() + "Target acquired.. ZAAAPP!!")
                tobar_out(get_energy_text() + "Charging laser...")
                tobar_out(get_energy_text() + "It's hard to tell now... but it seemed like some sort of massive insect")
            else:
                tobar_out(get_energy_text() + "Time to book it!")
                tobar["energy"] -= actions["run"]["cost"]
                tobar["hp"] -= 10
                if is_dead(): return True  # test if we are still alive
                tobar_out(get_energy_text() + "Whew... I'm glad I'm still alive, though I did get bumped around.")
        else:
            tobar_out(get_energy_text() + "I think its time to get out of here...")


# Code logic process
def run():
    continuing = True
    # saves his death place. used to seem like tobar is aware of failed attempts
    death_cell = {"x": -1, "y": -1}

    while continuing:  # used to allow a try again feature...
        init()
        commands_help()
        while not is_dead():
            # repeat until we get a valid command
            needs_input = True
            while needs_input and not is_dead():  # glitchy performance if I don't test is_dead() again here...

                # makes tobar aware of last death place
                tobar_out(get_energy_text() + terrain[tobar["y"]][tobar["x"]].entryText)
                if tobar["x"] == death_cell["x"] and tobar["y"] == death_cell["y"]:
                    tobar_out("Hmm. For a second there I thought I remembered dying here... I must have crossed wires.")
                response = get_input("What should I do?")

                # if testing different actions while still on the map
                if "/help" in response:
                    commands_help()
                elif "look" in response:
                    tobar["energy"] -= actions["look"]["cost"]  # remove the energy loss due to assumed travel
                    tobar_out(get_energy_text() + terrain[tobar["y"]][tobar["x"]].availableActions["look"])
                    needs_input = False

                    # start first secret dialog
                    if tobar["x"] == 0 and tobar["y"] == 0:
                        if "yes" in get_input("Should I enter the cave? (yes/no)"):
                            explore_tunnel()
                            if is_dead(): break

                    # start second secret dialog
                    if tobar["x"] == 2 and tobar["y"] == 1:
                        tobar["energy"] -= actions["go"]["cost"]/2
                        explore_city()
                        if is_dead(): break

                elif "scan" in response:  # print more info
                    tobar["energy"] -= actions["scan"]["cost"]  # remove the energy loss due to assumed travel
                    tobar_out(get_energy_text() + terrain[tobar["y"]][tobar["x"]].availableActions["scan"])
                    needs_input = False
                    if is_dead(): break
                elif "go" in response:
                    needs_input = False
                    tobar["energy"] -= actions["go"]["cost"]  # remove the energy loss due to assumed travel
                    if is_dead(): break  # tobar ran out of energy
                    if "north" in response:
                        # test to ensure we are within northern boundary
                        if tobar["y"] < 2:
                            tobar["y"] += 1
                            tobar_out(actions["go"]["run"])
                        else:
                            # handle out of boundary movements
                            print(formats["TOBAR"] + "I can't. The ravine is too steep.")
                            needs_input = True  # undo this change since we need to try again
                            tobar["energy"] += actions["go"]["cost"]  # undo the energy loss due to assumed travel
                    elif "south" in response:
                        if tobar["y"] > 0:
                            tobar["y"] -= 1
                            tobar_out(actions["go"]["run"])
                        else:
                            print(formats["TOBAR"] + "Won't do. The river would fry my circuits.")
                            needs_input = True  # undo this change since we need to try again
                            tobar["energy"] += actions["go"]["cost"]  # undo the energy loss due to assumed travel
                    elif "west" in response:
                        if tobar["x"] > 0:
                            tobar["x"] -= 1
                            tobar_out(actions["go"]["run"])
                        else:
                            print(formats["TOBAR"] + "I can't. The ground is so jagged its impassable.")
                            needs_input = True  # undo this change since we need to try again
                            tobar["energy"] += actions["go"]["cost"]  # undo the energy loss due to assumed travel
                    elif "east" in response:
                        if tobar["x"] < 2:
                            tobar["x"] += 1
                            tobar_out(actions["go"]["run"])
                        else:
                            print(formats["TOBAR"] + "I can't. my path is blocked.")
                            needs_input = True  # undo this change since we need to try again
                            tobar["energy"] += actions["go"]["cost"]  # undo the energy loss due to assumed travel
                    else:
                        tobar_out("Invalid direction... lets try again.")
                        needs_input = True  # undo this change since we need to try again
                        tobar["energy"] += actions["go"]["cost"]  # undo the energy loss due to assumed travel

            # if we died to damage...
            if tobar["hp"] <= 0:
                tobar["death_counter"] += 1
                death_cell["x"] = tobar["x"]
                death_cell["y"] = tobar["y"]
                tobar_out("AAHHH!!")
                sleep(delay_time() * 2)
                print(f"{formats['INFO']}Lost connection with user: TOBAR")
                sleep(delay_time())
                print(f"{formats['ERROR']}Error: Ansible connection terminated: unknown reason")
                sleep(1)
                print(f"{formats['SYS']}Powering down Ansible unit ", end="")
                slow_print(".....")
                print("Powering down ", end="")
                slow_print(".....", delay=st_delay/1.5)
                break

            # if we died to energy loss
            elif tobar["energy"] <= 0:
                tobar["death_counter"] += 1
                death_cell["x"] = tobar["x"]
                death_cell["y"] = tobar["y"]
                tobar_out("battery depleted must re... ")
                print(f"{formats['INFO']}User: TOBAR has powered down its communication system")
                sleep(delay_time())
                print(f"{formats['ERROR']}Error: Ansible connection terminated: Client disconnected")
                sleep(1)
                print(f"{formats['SYS']}Powering down Ansible unit ", end="")
                slow_print(".....")
                print("Powering down ", end="")
                slow_print(".....", delay=st_delay/1.5)
                break

        print("\n\n\t\t\t GAME OVER\n\n")

        if "yes" in get_input("Would you like to try again? (yes/no)").lower():
            # reset crucial data
            tobar["energy"] = 100
            tobar["hp"] = 100
            tobar["x"] = 1
            tobar["y"] = 1
            world["city_visited"] = False
            # If the user wants to continue, just go ahead and repeat the while
        else: continuing = False  # otherwise we will break


# actually run the game
run()
