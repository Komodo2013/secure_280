# Lets the user pick the shape we are working with and prints the area to terminal.

# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
import math

# Dictionary holding useful colors for terminal output
form = {
    "g": "\x1b[0;92;48m",
    "w": "\x1b[0;97;48m",
    "y": "\x1b[0;93;48m",
    "r": "\x1b[0;91;48m",
    "grey": "\x1b[0;37;48m",
}


# Dictionary holding each shape, parameters to ask for and the equation
shapes = {
    # Shape
    "square": {
        # Shape name, used in search with user input
        "name": "square",
        # Parameters to ask for
        "sides": [
            "Side: "
        ],
        # Equation to calculate the area
        "equation": lambda values: shapes["rectangle"]["equation"]([values[0], values[0]])
    },
    "triangle": {
        "name": "triangle",
        "sides": [
            "Base: ",
            "Height: "
        ],
        "equation": lambda values: values[0] * values[1] * .5
    },
    "rectangle": {
        "name": "rectangle",
        "sides": [
            "Length: ",
            "Height: "
        ],
        "equation": lambda values: values[0] * values[1]
    },
    "parallelogram": {
        "name": "parallelogram",
        "sides": [
            "Length: ",
            "Width: "
        ],
        "equation": lambda values: shapes["rectangle"]["equation"](values)
    },
    "trapezoid": {
        "name": "trapezoid",
        "sides": [
            "Base: ",
            "Top Length: ",
            "Height: "
        ],
        "equation": lambda values: (values[0] + values[1]) * values[2] / 2
    },
    "ellipse": {
        "name": "ellipse",
        "sides": [
            "Radius 1: ",
            "Radius 2: "
        ],
        "equation": lambda values: values[0] * values[1] * math.pi
    },
    "circle": {
        "name": "circle",
        "sides": [
            "Radius: "
        ],
        "equation": lambda values: values[0] ** 2 * math.pi
    },
    "kite": {
        "name": "kite",
        "sides": [
            "Side 1: ",
            "Side 2: "
        ],
        "equation": lambda values: values[0] * values[1] / 2
    },
    "rhombus": {
        "name": "rhombus",
        "sides": [
            "Side 1: ",
            "Side 2: "
        ],
        "equation": lambda values: shapes["kite"]["equation"](values)
    },
    "equilateral_triangle": {
        "name": "equilateral triangle",
        "sides": [
            "Side: ",
        ],
        "equation": lambda values: values[0] ** 2 / 4 * 3 ** .5
    },
    "pentagon": {
        "name": "pentagon",
        "sides": [
            "Apothem: ",
        ],
        "equation": lambda values: values[0] ** 2 * 5/8 * (10 + 2 * 5 ** .5) ** .5
    },
    "hexagon": {
        "name": "hexagon",
        "sides": [
            "Side: ",
        ],
        "equation": lambda values: values[0] ** 2 * 3 ** .5
    },
    "octagon": {
        "name": "equilateral triangle",
        "sides": [
            "Side: ",
        ],
        "equation": lambda values: values[0] * 6.64
    },
    "circle_slice": {
        "name": "slice of a circle",
        "sides": [
            "Radius: ",
            "Arc Length: "
        ],
        "equation": lambda values: values[0] * values[1] * .5
    },
    "circle_segment": {
        "name": "segment of a circle",
        "sides": [
            "Radius: ",
            "Angle (in degrees): "
        ],
        "equation": lambda values: 2 * values[0] * math.sin(.5 * math.radians(values[1]))
    },
    "heptagon": {
        "name": "heptagon",
        "sides": [
            "Side: ",
        ],
        "equation": lambda values: values[0] ** 2 * 7/4 * math.atan(math.radians(180/7))
    }
}


# Error to throw if user input doesn't match a known shape
class ShapeNotFound(Exception):
    """
        Error raised when the program could not find a defined shape by name
    """
    pass


def get_input(s=""):
    """
        Wrapper of print and input. The format will be s -> _
        :param s: String the text to display before asking for input:
        :returns: String The user's input stripped of whitespace on both sides
    """
    return input(form["w"] + s + "\t\u2192 ").strip().lower()


def get_sides_for_shape(s: str):
    """
        finds shape matching string s and loops through each parameter, asking for input. Returns list
        :param s: String the name of the shape we are finding the surface area for
        :returns: list containing the parameters needed to preform the calculations
    """
    # list we will return
    sides_ = []

    # test each shape in the shapes for a name match
    for entry in shapes.values():
        if entry['name'] in s:
            # Ask for the value of each prompt stored in sides
            for item in entry['sides']:
                sides_.append(float(get_input(item)))
            return sides_
    # if we are here, no match was found so throw and exception
    raise ShapeNotFound


def get_area(s: str, values: list):
    """
        calculates the area of shape named s using its equation
        :param s: String the name of the shape to use
        :param values: list the parameters to use to calculate the area
        :returns: float the value of the area
    """
    # iterate over shapes looking for our shape s
    for entry in shapes.values():
        if entry['name'] in s:
            # execute and return the result of the area equation
            return entry['equation'](values)


# Get shape
shape = get_input("What kind of shape would you like to find the area of? (or type end to stop)")
while "end" not in shape:
    # try/catch to account for value error and ShapeNotFound
    try:
        sides = get_sides_for_shape(shape)
        area = get_area(shape, sides)
        print(f"The area of this {form['g']}{shape}{form['w']} is: {form['g']}{area}{form['w']}")
    except ShapeNotFound:
        print(f"{form['r']}Couldn't find a shape with name: {form['g']}{shape}{form['w']}")
    except ValueError:
        print(f"{form['r']}Couldn't convert input into numbers{form['w']}")

    shape = get_input("What kind of shape would you like to find the area of? (or type end to stop)")
