# Function that calculates and then displays a graph of wind chill based off user given temperature
# Since I've been using functions throughout the term, I decided to stretch some more and use lambda expressions
import matplotlib.pyplot as plot
import numpy


# Useful colors for printing to terminal
form = {
    "g": "\x1b[0;92;48m",
    "w": "\x1b[0;97;48m",
    "y": "\x1b[0;93;48m",
    "r": "\x1b[0;91;48m",
    "grey": "\x1b[0;37;48m",
}


# Dictionary with useful functions for conversion and windchill
equations = {
    "to_f": lambda t: t * 9/5 + 32,
    "to_c": lambda t: (t - 32) * 5/9,
    "chill": lambda t, v: 35.74 + .6215 * t - 35.75 * v ** .16 + .4275 * t * v ** .16
}


""" # I put these functions here just to fulfill the requirements I don't actually use these, so I commented them out.
def to_fahrenheit(c):
    return c * 9/5 + 32


def to_celsius(f):
    return (f - 32) * 5/9


def get_windchill(t, v):
    return 35.74 + .6215 * t - 35.75 * v ** .16 + .4275 * t * v ** .16
"""


def get_input(s=""):
    """
        Wrapper of print and input. The format will be s -> _
        :param s: String the text to display before asking for input:
        :returns: String The user's input stripped of whitespace on both sides
    """
    return input(form["w"] + s + "\t\u2192 ").strip().lower()


def graph(t: float, celsius = False):
    """
        Extrapolates the ambient temperature t to get windchill values. Graphs data and prints 5mph intervals
        :param t: Float the ambient temperature
        :param celsius: Boolean whether we are using celsius for temperature
    """
    # Convert user inputted C to F
    if celsius:
        t = equations["to_f"](t)

    # Generate an array for x steps from 0 to 60
    x = numpy.arange(0, 60.1, .1)
    # Evaluate the windchill equations for ambience t and speed x
    y = equations["chill"](t, x)

    # ensure that the windchill isn't greater than the ambient temperature
    adjuster = numpy.vectorize(lambda v: min(t, v))
    y = adjuster(y)

    # Label for the units
    label = "°F"

    # If we are working with celsius, convert t and y back to c to display, also change the label
    if celsius:
        t = equations["to_c"](t)
        y = equations["to_c"](y)
        label = "°C"

    # Print header
    print(f"{form['w']}Displaying windchill for ambient temperature: {form['g']}{t:2.2f}{label}{form['w']}")
    # Get the iterable lists from numpy
    temp_x = numpy.array(x)
    temp_y = numpy.array(y)
    # print every 50th value of the equations. this yields 5 mph increments = every 50th * .1 step length
    for i in range(len(temp_y)):
        if i % 50 == 0:
            print(f"Windchill @{form['g']}{temp_x[i]: 1.1f}{form['w']}: {form['g']}{temp_y[i]:2.2f}{label}{form['w']}")

    # Stuff to make the plot work
    plot.plot(x, y)
    plot.xlabel("Wind Speed - MPH")
    plot.ylabel("Windchill - " + label)
    plot.title(f"Windchill of {t:2.2f}{label} Ambient Temperature")

    plot.show()


# Get user input. we expect ##.##(f/c) or end
text = get_input("Please input the ambient temperature followed by F/C for unit. Type end to end")
while "end" not in text:
    try:
        # Assume we are not in celsius unless we include c
        celsius = False
        if "c" in text:
            celsius = True

        # get the number from the text after removing the c or f
        ambient = float(text.strip("c").strip("f"))

        # this function actually does all the stuff we need, including display
        graph(ambient, celsius = celsius)

    # we don't have to do anything if error, just ask again
    except ValueError:
        print(f"{form['r']}Error while parsing input. Please enter a number followed by an F/C or 'end' to finish")

    # get new user input for next loop
    text = get_input("\nPlease input the ambient temperature followed by F/C for unit. Type end to end")
