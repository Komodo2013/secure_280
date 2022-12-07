
def galois_multiply(a, b):
    p = 0x00
    for i in range(8):
        if b & 0x01 == 0x01:
            p ^= a
        b = b >> 1
        if a & 0x80 == 0x80:
            a = (a << 1) % 256
            a ^= 0x1b
        else:
            a = (a << 1) % 256
    return p


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


"""g = Galois()
print(g.look_ups)
print(g.multiply(5, 9))"""
