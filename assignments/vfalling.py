# Group project, calculates the velocity of an object in free fall after time t
# Imports
import math


# This is all my functions I've already been using...

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
def get_format(style_type):
    return "\x1b[%sm" % style_type


# Wrapper of print and set_format
# @param s String message to print to terminal and gets user input
# @returns in String whatever the user typed
def get_input(s=""):
    return input(get_format(formats["SYS"]) + s + "\t\u2192 ").strip()


# Dictionary holding various acceleration values for different planets in m/s/s
acceleration = {
    "sun": 274.13,
    "mercury": 3.59,
    "venus": 8.87,
    "earth": 9.81,
    "moon": 1.62,
    "mars": 3.77,
    "jupiter": 25.95,
    "saturn": 11.08,
    "uranus": 10.67,
    "neptune": 14.07,
    "pluto": 0.42
}


# Dictionary of various drag coefficients for objects
drag = {
    "sphere": .5,
    "bird": .4,
    "hemisphere": .42,
    "cube": .8,
    "person": 1.0,
    "person_upright": 1.3,
    "streamlined": .1,
    "cylinder": 1.1,
}


# Dictionary of various fluid densities - in kg/m^3
densities = {
    "air": 1.3,
    "water": 1000,
}

# initialize variables
mass = g = t = density = area = drag_constant = 0


# Dictionary of preset scenarios, to skip having to enter it all
presets = {
    "skydiver": {
        "mass": 62,
        "gravity": acceleration["earth"],
        "density": densities["air"],
        "cross_section": .45,
        "drag": drag["person"]
    },
    "ball": {
        "mass": 5,
        "gravity": acceleration["earth"],
        "density": densities["air"],
        "cross_section": .01,
        "drag": drag["sphere"]
    },
    "bowling-ball": {
        "mass": 5.455,
        "gravity": acceleration["earth"],
        "density": densities["air"],
        "cross_section": .0366,
        "drag": drag["sphere"]
    },
    "astronaut-moon": {
        "mass": 62,
        "gravity": acceleration["moon"],
        "density": .001,
        "cross_section": .45,
        "drag": drag["person"]
    },
    "astronaut-jupiter": {
        "mass": 62,
        "gravity": acceleration["jupiter"],
        "density": .1326,
        "cross_section": .45,
        "drag": drag["person"]
    }
}


print(get_format(formats["SYS"]) + "Ready to calculate velocity of free falling objects.")

found = "Found the following presets: \t" + get_format(formats["green"])
for pre in presets:
    found += pre + ", "

found = found[:-2]  # removes the last ", "
print(found)
choice = get_input("Please enter the name of a preset or hit enter for custom").lower()

if choice in presets:
    # just loading values from preset dictionary
    mass = presets[choice]["mass"]
    g = presets[choice]["gravity"]
    density = presets[choice]["density"]
    area = presets[choice]["cross_section"]
    drag_constant = presets[choice]["drag"]
    t = float(get_input("You would like to know the velocity after how many seconds?"))
else:
    # get inputs
    mass = float(get_input("Mass in kg"))
    g = float(get_input("Acceleration due to gravity in m/s^s (9.81 for Earth, 24 for Jupiter)"))
    density = float(get_input("Density of the fluid in kg/m^3 (1.3 for air, 1000 for water)"))
    area = float(get_input("Cross sectional area in m^2"))
    drag_constant = float(get_input("Drag constant (.5 for sphere, 1.1 for cylinder)"))
    t = float(get_input("You would like to know the velocity after how many seconds?"))


# v(t) = (mg/c)^.5 * (1 - e^((mgc)^.5 * -t/m)) where c = .5dak
c = .5 * density * area * drag_constant
# terminal velocity = (mg/c)^.5 since lim t->inf of e^((mgc)^.5 * -t/m) = 0
terminalV = math.sqrt(mass * g / c)
# calculate v(t)
v = terminalV * (1 - math.exp(math.sqrt(mass * g * c) * -t / mass))

green = get_format(formats["green"])
sys = get_format(formats["SYS"])

print("\n-----------------------------------------------")

# display results
print(f"The inner value of c is: {green}{c:.3f}{sys}")
print(f"The velocity after {green}{t:.1f}{sys} seconds is: {green}{v:.3f}{sys} m/s")
print(f"The terminal velocity is: {green}{terminalV:.3f} m/s")
