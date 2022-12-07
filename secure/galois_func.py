def galois_multiply(a, b):
    p = 0x00
    for i in range(8):
        if b & 0x01 == 0x01:
            p ^= a
        b = b >> 1
        if a & 0x80 == 0x80:
            a = (a << 1) & 0xff
            a ^= 0x1b
        else:
            a = (a << 1) & 0xff
    return p


def big_galois_multiply(a, b):
    p = 0x00
    for i in range(256):
        if b & 0x01 == 0x01:
            p ^= a
        b = b >> 1
        if a & 0x80 == 0x80:
            a = (a << 1) & 0xff
            a ^= 0x1b
        else:
            a = (a << 1) & 0xff
    return p


"""Functions gf_degree and galois_inv retrieved from stackoverflow.com 8th of Apr 2022
https://stackoverflow.com/questions/45442396/a-pure-python-way-to-calculate-the-multiplicative-inverse-in-gf28-using-pytho
by redit user Jonas https://stackoverflow.com/users/2378300/jonas
answered 1 Aug 2017"""
def gf_degree(a):
    res = 0
    a >>= 1
    while a != 0:
        a >>= 1
        res += 1
    return res


def galois_inv(a, mod=0x1B):
    v = mod
    g1 = 1
    g2 = 0
    j = gf_degree(a) - 8

    while a != 1:
        if j < 0:
            a, v = v, a
            g1, g2 = g2, g1
            j = -j

        a ^= v << j
        g1 ^= g2 << j

        a %= 256   # Emulating 8-bit overflow
        g1 %= 256  # Emulating 8-bit overflow

        j = gf_degree(a) - gf_degree(v)

    return g1


def galois_divide(a, b):
    return galois_multiply(a, galois_inv(b))


def galois_add(a, b):
    return a ^ b



class Galois:

    # 2, 3, 9, 11, 13, 14
    look_indexes = [2, 3, 9, 11, 13, 14]
    look_inv = [-1, -1, 0, 1,
                -1, -1, -1, -1,
                -1, 2, -1, 3,
                -1, 4, 5, -1]
    look_ups = []

    def __init__(self):
        for i in self.look_indexes:
            self.look_ups.append([])
            for j in range(256):
                self.look_ups[-1].append(galois_multiply(j, i))

    def multiply(self, a, b):
        if self.look_inv[b] == -1:
            return a
        return self.look_ups[self.look_inv[b]][a]


def galois_big_inv(a, mod=2**256):
    v = mod
    g1 = 1
    g2 = 0
    j = gf_degree(a) - 8

    while a != 1:
        if j < 0:
            a, v = v, a
            g1, g2 = g2, g1
            j = -j

        a ^= v << j
        g1 ^= g2 << j

        a %= 2**256   # Emulating overflow
        g1 %= 2**256  # Emulating overflow

        j = gf_degree(a) - gf_degree(v)
        # print(a, g1)
    return g1
