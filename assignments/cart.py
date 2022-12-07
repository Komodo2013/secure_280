# Shopping cart system in python
# Here is just a random list of stuff I can do to this program if I get around to it
# TODO: move view total as part of view cart
# TODO: add new menu option edit item
# TODO: allow add item to just increase quantity if you add same item twice
# TODO: allow remove item to remove x quantity
# DONE: add code from checkout in mealCals.py to end
# TODO: use tkinter to give this an actual GUI


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
    for i, d in menuItems.items():
        # boolean if this option should be greyed out - if there are no items in cart, can't remove/display
        grey_out = len(myCart.cart) == 0 and not (i == "2" or i == "6")

        # add grey format
        if grey_out: menu_text += f"{form['grey']}"
        # add the menu item, as well as it's display index
        menu_text += f"{i}. {d['text']} \t\t"
        # return to white
        if grey_out: menu_text += f"{form['w']}"

    # display menu
    print(menu_text)

    # get the user input
    val = get_input("")
    # iterate through each menu item and test if the number (as string) and
    for i, d in menuItems.items():
        if val in i:
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


change = {
    "100": {
        "val": 100.,
        "print": "$100"
    },
    "20": {
        "val": 20.,
        "print": "$20"
    },
    "10": {
        "val": 10.,
        "print": "$10"
    },
    "5": {
        "val": 5.,
        "print": "$5"
    },
    "1": {
        "val": 1.,
        "print": "$1"
    },
    ".25": {
        "val": .25,
        "print": "$0.25"
    },
    ".10": {
        "val": .1,
        "print": "$0.10"
    },
    ".05": {
        "val": .05,
        "print": "$0.05"
    },
    ".01": {
        "val": .01,
        "print": "$0.01"
    }
}


def purchase_func():
    """
        Function run from menu. asks for payment amount and then returns the change, terminates the loop
        :returns: Boolean False
    """
    # Test if cart is empty, if so say cart is empty and return to menu
    if len(myCart.cart) == 0:
        print(f"{form['y']}\t\u2192 Your Cart is empty! \u2190")
        return True

    payment_type = get_input("How would you like to pay for your items? (card/cash)").lower()
    if "cash" in payment_type:
        try:
            change_amount = 0.0
            not_enough = True
            while not_enough:
                change_amount = float(get_input("Payment amount")) - myCart.get_total()
                if change_amount >= 0:
                    not_enough = False
                else:
                    print(f"{form['y']}Not enough cash! Must be more than: ${form['r']}{myCart.get_total()}{form['w']}")

            change_string = ""

            for denominator in change.values():
                count = int(change_amount / denominator['val'])
                if count >= 1:
                    change_string += f"\t{denominator['print']} - {form['g']}{count}{form['w']}"
                    change_amount = change_amount % denominator['val']
            view_func()
            view_total()
            print(change_string)

        except ValueError:
            pass

    print("\n\t\tThanks for your purchase! Goodbye")
    return False


def exit_func():
    """
        Function run from menu. Prints bye and returns false, terminating the loop
        :returns: Boolean False
    """
    print("\n\t\t\tGoodbye!")
    return False


def view_func():
    """
        Function run from menu. Displays all items in the cart
        :returns: Boolean True
    """
    print(f"{form['w']}Here is a listing of the items in your cart:")

    # Test if cart is empty, if so say cart is empty and return to menu
    if len(myCart.cart) == 0:
        print(f"{form['y']}\t\u2192 Your Cart is empty! \u2190")
        return True

    # string to save each formatted cart item
    listing = ""
    # Counter for line numbers
    num = 0
    # Iterate over each item in cart
    for item in myCart.cart:
        num += 1
        # separated in order to pad with spaces to 20 characters
        name = item['name'].ljust(20)
        # Formats to #. Item  quantity @ $##
        listing += f"{form['w']}{num}. {name}\t{form['g']}{item['quantity']:3}{form['w']} @ {form['g']}" \
            f"{item['price']:3.2f}\n"
    print(listing)
    # continue looping
    return True


def remove_func():
    """
        Function run from menu. Asks for and then removes an item from the cart
        :returns: Boolean True
    """
    # If nothing in cart, say nothing in cart and return
    if len(myCart.cart) == 0:
        print(f"{form['y']}\t\u2192 Your Cart is empty! \u2190")
        return True

    # Get user input - all items are capitalized
    to_remove = get_input("Please enter the name or corresponding number of the item to remove: ").capitalize()

    # Try to convert to number - if successful then user inputted an index
    try:
        # remove 1 from user inputted index, as user doesn't see 0th index - starts at 1
        to_remove = int(to_remove) - 1
        if 0 <= to_remove < myCart.get_num_items():
            # remove the item from that index
            myCart.remove_index(to_remove)
    except ValueError:
        # If it was a string, lets try to parse the string
        myCart.remove_item_named(to_remove)

    # Return true to continue loop
    return True


def view_total():
    """
        Function run from menu. Displays the total num and cost of the cart
        :returns: Boolean True
    """
    # If nothing in cart say nothing in cart and return
    if len(myCart.cart) == 0:
        print(f"{form['y']}\t\u2192 Your Cart is empty! \u2190")
        return True

    # Print sum of parts
    print(f"{form['w']}Your cart has a total of: {form['g']}{myCart.get_num_items()}{form['w']} items totaling: "
          f"{form['g']}${myCart.get_total(): .2f}{form['w']}")
    return True


def add_func():
    """
        Function run from menu. Asks for and then adds data for a new item for the cart
        :returns: Boolean True
    """
    # Get name and format with capitalization
    name = get_input(f"{form['w']}Please input the name of the item:").capitalize()
    # get price as float
    price = float(get_input("Price per item? (don't include '$')"))
    # get quantity to buy
    quantity = int(get_input("How many?"))

    # add item to cart
    myCart.add_item_price(name, price, quantity)
    return True


# Cart class handles saving, editing and getting fo the shopping cart
# yes I realize I over-complicated it, but now it functions more like I'm used to
class Cart:
    def __init__(self):
        # used to save the array of items in the cart
        self.cart = []

    def add_item_price(self, item, price, quantity = 1):
        """
            Adds an item to the cart
            :param item: String the name of the item
            :param price: Float the cost of the item
            :param quantity: Int Optional the number of this item
            :returns self: this instance
        """
        self.cart.append({
            "name": item,
            "price": price,
            "quantity": quantity
        })
        return self

    def remove_item_named(self, name):
        """
            Removes an item from the cart by name
            :param name: String the name of the item to remove
            :returns self: this instance
        """
        # test name of each item in the cart
        for i in range(0, len(self.cart) - 1):
            if self.cart[i]['name'] in name:
                # pop the one we want to remove and return
                self.cart.pop(i)
                return self

        # If we are here, then we failed to find the item
        print(f"Item: {form['g']}{name}{form['w']} not found")
        return self

    def remove_index(self, index):
        """
            Removes an item from the cart by its index
            :param index: Integer the index of the item to remove
            :returns self: this instance
        """
        # If the index lies within the proper bounds of the cart array
        if 0 <= index < len(self.cart):
            # Remove index index
            self.cart.pop(index)
            return self
        else:
            # Otherwise that index doesn't exist
            print(f"{form['w']}No item in index: {form['g']}{index + 1}{form['w']}")
            return self

    def get_total(self):
        """
            Gets the sum total of items in cart
            :returns self: Float - Sum of all item prices
        """
        sum_ = 0
        for item in self.cart:
            sum_ += item["price"] * item["quantity"]
        return sum_

    # gets the sum total of items in cart
    # @returns float the sum of all items
    def get_num_items(self):
        """
            Gets the total number of items in cart
            :returns self: Int total number of items in cart
        """
        sum_ = 0
        for item in self.cart:
            sum_ += item["quantity"]
        return sum_


# Dictionary holding all menu options. This is place here as teh functions must be defined before they can be
# indexed in the dictionary
# display index: {text: name of menuItem, func: function to run if chosen}
menuItems = {
    "1": {
        "text": "View Cart",
        "func": view_func
    },
    "2": {
        "text": "Add item",
        "func": add_func
    },
    "3": {
        "text": "Remove item",
        "func": remove_func
    },
    "4": {
        "text": "View total",
        "func": view_total
    },
    "5": {
        "text": "Purchase",
        "func": purchase_func
    },
    "6": {
        "text": "Exit",
        "func": exit_func
    }
}

# Create a cart
myCart = Cart()

# While we want to run the program
continuing = True
while continuing:
    # get user input from menu, assigning the function as selection
    selection = menu()
    # execute the returned function, which returns whether to continue the loop
    continuing = selection()
