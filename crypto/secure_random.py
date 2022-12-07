"""
Gather entropy
X initialize as hash internal matrix - just needs to be a string or bytearray

generate number - can use bytes from the hash algorithm to get value
add salt to internal matrix - must be some mathematical operation, can gather entropy ever n operations?

"""
import time

import hash
from ctypes import windll, Structure, c_long, byref
from time import sleep
from random import randrange


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def askWithTimer(prompt):
    print(prompt)
    start = time.time()
    response = input().strip()
    return {'x': response, 'y': "", 't': time.time() - start}


def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}


def get_entropy(iterations, time, use_questions):
    mouse_points = []
    responses = []

    questions = ["Favorite food?", "Ideal place to live", "Childhood friend", "Favorite animal", "Your ideal car"]

    if use_questions:
        print("Gathering random responses, answer each prompt, answers may be random")
        for i in range(int((iterations / 3) % len(questions))):
            question_num = randrange(0, len(questions), 1)
            responses.append(askWithTimer(questions[question_num]))
            questions.pop(question_num)

    print("Gathering entropy, please move cursor around")

    for i in range(iterations):
        t = 0
        pos = queryMousePosition()
        t = randrange(1, time * 100, 1) / (iterations * 100)

        if i >= 1:
            same = True

            while same:
                sleep(t)
                pos = queryMousePosition()
                pos['t'] = t
                if pos['x'] != mouse_points[i-1]['x'] and pos['y'] != mouse_points[i-1]['y']:
                    same = False
                t = randrange(1, time, 1) / (iterations * 100)
        else:
            sleep(t)
            pos = queryMousePosition()
            pos['t'] = t

        mouse_points.append(pos)


    if use_questions:
        i = 1
        for q in responses:
            mouse_points.insert(i, q)
            i += 2

    points = ""
    for p in mouse_points:
        points += str(p['x']) + str(p['y']) + str(p['t'])

    return points


class SecureRandom:

    def __init__(self, entropy, is_packet = False):
        if is_packet:
            self.hasher = hash.MyHash()
            for i in range(8):
                self.hasher.internal_matrix[i] = entropy[i][:]
        else:
            self.hasher = hash.MyHash().set_internal_matrix(entropy)
        self.since_entropy = 0

    def addSalt(self):
        if self.since_entropy >= 5:
            entropy = get_entropy(10, 1, False)
            self.hasher.set_internal_matrix(self.hasher.hash_packs(entropy, 40))
            self.since_entropy = 0

        salt = hash.hash_(self.hasher.internal_matrix, 20)
        self.hasher.set_internal_matrix(hash.packet_to_alpha_numeric(salt))

    def get_rand(self):
        my_bytes = bytearray()

        for r in range(4):
            for b in range(len(self.hasher.internal_matrix[r])):
                my_bytes.append(self.hasher.internal_matrix[r][b] ^ self.hasher.internal_matrix[r + 4][b])

        self.addSalt()
        return int.from_bytes(my_bytes, "big") / 2 ** (8 * 32)

    def get_rand_int(self, max, min = 0):
        my_bytes = bytearray()
        half = int(len(self.hasher.internal_matrix) / 2)

        for r in range(half):
            for b in range(len(self.hasher.internal_matrix[r])):
                my_bytes.append(self.hasher.internal_matrix[r][b] ^ self.hasher.internal_matrix[r + half][b])

        self.addSalt()
        return (int.from_bytes(my_bytes, "big") % (max - min)) + min


"""
entropy = get_entropy(100, 10, True)
my_secure_random = SecureRandom(entropy)

print(hash.packet_to_alpha_numeric(my_secure_random.hasher.internal_matrix))
for i in range(50):
    my_secure_random.get_rand_int(100)
    print(hash.packet_to_alpha_numeric(my_secure_random.hasher.internal_matrix))
"""
