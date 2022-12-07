topics = {"Color", "Pass Time", "Food", "Work"}
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

for t in topics:
    print(t)

if "red" in formats: print("Yeah")
