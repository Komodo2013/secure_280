

# Dictionary holding useful format variables. They get changed as you play
# Stored in format int;int;int except when all are 0, which reduces to 0
form = {
    "g": "\x1b[0;92;48m",
    "w": "\x1b[0;97;48m",
    "y": "\x1b[0;93;48m",
    "grey": "\x1b[0;37;48m",
}


def get_input(s=""):
    """
        Wrapper of print and input. The format will be s -> _
        :param s: String the text to display before asking for input:
        :returns: String The user's input stripped of whitespace on both sides
    """
    return input(form["w"] + s + "\t\u2192 ").strip()


def get_account_info():
    """
        Asks for account name and balance. If name returned is continue/quit then returns 0. If error on float(balance)
        returns -1 for redo. Otherwise returns 1, name, balance
        :returns: Int return code: -1 for ValueError, 0 for break, 1 if values for name/balance
        :returns name: String the name of the account
        :returns balance: Float balance of the account
    """
    account_name = get_input("Name")

    if "continue" in account_name or "quit" in account_name:
        return 0, False, False

    try:
        account_balance = float(get_input("Balance"))
    except ValueError:
        return -1, False, False

    return 1, account_name, account_balance


def print_accounts(print_all):
    """
        Prints the name and balance of each account, and if print_all then print total, average, and high.
        :param print_all: Boolean True whether to print all values or not.
        :return:
    """
    total = 0
    high = {"name": "", "balance": 0}
    account_list = ""
    for i in range(len(accounts)):
        formatted = accounts[i]['name'].ljust(20)
        total += accounts[i]['balance']
        if accounts[i]['balance'] > high['balance']:
            high = accounts[i]
        account_list += f"\n{form['w']}{i + 1}. {formatted} - {form['g']}${accounts[i]['balance']}"

    if print_all:
        print(f"{form['w']}Total: {form['g']}${total:.2f}")
        print(f"{form['w']}High: {high['name']} - {form['g']}${high['balance']:.2f}")
        print(f"{form['w']}Average: {form['g']}${total/len(accounts) : .2f}")

    print(account_list)


print(f"{form['w']} Please enter the names and balances of your accounts. Type continue when done")


continuing = 1
accounts = []
while continuing != 0:
    continuing, name, balance = get_account_info()

    if continuing == -1:
        print(f"{form['y']}Sorry, balance entered was not a number. Please try again{form['w']}")

    if continuing == 1:
        accounts.append({
            "name": name,
            "balance": balance
        })

print_accounts(True)

while "y" in get_input("Update an account? (y/n)").lower():
    try:
        index = int(get_input("Of account number?")) - 1
        amount = float(get_input("New balance?"))
        accounts[index]['balance'] = amount
        print_accounts(False)
    except ValueError:
        print(f"{form['y']}Invalid input. Please try again.{form['w']}")
