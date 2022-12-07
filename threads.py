from threading import Thread
from time import sleep

result = None


def update_every_second():
    global waited
    if not waited:
        waited = 0
    while result is None:
        sleep(1)
        waited += 1
        if waited >=20:
            print("Hello?")

t = Thread(target=update_every_second)
t.start()
result = input('Yes?')
waited = 0

print("The user typed", result)