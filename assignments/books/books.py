# Opens books.txt and then prints data as a pretty list


def get_input(s=""):
    """
        Wrapper of print and input. The format will be s -> _
        :param s: String the text to display before asking for input:
        :returns: String The user's input stripped of whitespace on both sides
    """
    return input(form["w"] + s + "\t\u2192 ").strip()


def menu():
    """
        Function run from menu. Displays menu of actions, gets user input and returns the corresponding function
        :returns: Function the function corresponding to the menuItem selected
    """
    print(f"{form['w']}\nSelect an option by entering the corresponding number:")

    # String to put menu in
    menu_text = ""
    # For each menu item
    for j, d in menuItems.items():
        # add the menu item, as well as it's display index
        menu_text += f"{j}. {d['text']} \t\t"

    # display menu
    print(menu_text)

    # get the user input
    val = get_input("")
    # iterate through each menu item and test if the number (as string) and
    for j, d in menuItems.items():
        if val in j:
            # return the driving function for this ch
            return d['func']


# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
form = {
    "g": "\x1b[0;92;48m",
    "w": "\x1b[0;97;48m",
    "y": "\x1b[0;93;48m",
    "r": "\x1b[0;91;48m",
    "grey": "\x1b[0;37;48m",
}


def exit_func():
    """
        Function run from menu. Prints bye and returns false, terminating the loop
        :returns: Boolean False
    """
    print("\n\t\t\tGoodbye!")
    return False


def total_func():
    largest_num = 0
    largest_name = ""
    for entry in data:
        if entry["Chapters"] > largest_num:
            largest_num = entry["Chapters"]
            largest_name = entry["Name"]
    print(f"{form['w']}The largest book by chapter is: {form['g']}{largest_name}{form['w']} with"
          f" {form['g']}{largest_num}{form['w']} chapters.")
    return True


def by_book_func():
    book = get_input("Which book do you want to search?")

    largest_num = 0
    largest_name = ""
    for entry in data:
        if entry["Book"] in book and entry["Chapters"] > largest_num:
            largest_num = entry["Chapters"]
            largest_name = entry["Name"]
    print(f"{form['w']}The largest book in {form['g']}{book}{form['w']} by chapter is: {form['g']}{largest_name}"
          f"{form['w']} with {form['g']}{largest_num}{form['w']} chapters.")
    return True


# Dictionary holding all menu options. This is place here as teh functions must be defined before they can be
# indexed in the dictionary
# display index: {text: name of menuItem, func: function to run if chosen}
menuItems = {
    "1": {
        "text": "Total analysis",
        "func": total_func
    },
    "2": {
        "text": "Search by book",
        "func": by_book_func
    },
    "3": {
        "text": "Exit",
        "func": exit_func
    }
}


data = []
with open("books_and_chapters.txt") as file:
    for line in file:
        item = line.strip().split(":")
        for i in range(len(item)):
            item[i] = item[i].strip()
        print(f"{form['w']}{item[2]}, Book: {item[0]}, Chapters: {item[1]}")
        data.append({
            "Book": item[2],
            "Name": item[0],
            "Chapters": int(item[1])
        })


# While we want to run the program
continuing = True
while continuing:
    # get user input from menu, assigning the function as selection
    selection = menu()
    # execute the returned function, which returns whether to continue the loop
    continuing = selection()
