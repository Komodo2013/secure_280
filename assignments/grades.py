# Simple program printing letter grade from percent

# use while statement for faster use
while True:
    # Get percent to use, turn into a float
    v = float(input("Enter grade percent \t -> "))
    # Beginning of message which ends as "You got a __"
    msg = "You got a"

    # Simple switch case for each letter
    if v >= 90.0: msg += "n A"  # This one is special cause a A -> an A
    elif v >= 80.0: msg += " B"
    elif v >= 70.0: msg += " C"
    elif v >= 60.0: msg += " D"
    else: msg += " F"

    # Take modulo 10 of percent to get ones place
    partial = v % 10
    # If greater than 7 and not an A or F, add a plus
    if partial >= 7.0:
        if v <= 90.0 or v < 60:
            msg += "+"
    elif partial < 4.0 and not v < 60:  # add minus if it isn't an F, otherwise do nothing
        msg += "-"

    # Print message
    print(msg)

    # Print if passed class (grade > 70)
    if v >= 70.0: print("Yay! You passed the class!!")
    else: print("Looks like you didn't pass. That's ok, just do better next time!")
