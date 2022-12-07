def c_shift(b, n):
    """
    Cyclically shifts a byte left n bits
    :param b: the byte to shift
    :param n: the number of bits to shift
    :return: byte after shifting
    """
    return ((b << n) % 256) | (b >> (8 - n))


def s_box_function(b):
    """
    Substitution calculation, able to run fairly quickly. Unfortunately, the function does not return the values
    stated by the wiki page on "Rijndael S-box". bytes are mapped, so one byte always returns one other byte
    :param b: the byte to substitute
    :return: byte after substitution
    """
    return b ^ c_shift(b, 1) ^ c_shift(b, 2) ^ c_shift(b, 3) ^ c_shift(b, 4) ^ 99


def inv_s_box_function(b):
    """
    Inverse substitution calculation, able to run fairly quickly. Unfortunately, the function does not return the values
    stated by the wiki page on "Rijndael S-box". Incidentally, it does undo the s_box_function(), so still works =D
    :param b: the byte to substitute
    :return: byte after substitution
    """
    return c_shift(b, 1) ^ c_shift(b, 3) ^ c_shift(b, 6) ^ 0x05


class SubsBoxes:
    """
    Contains the functions necessary for dealing with byte substitutions
    """

    s_box = []
    i_box = []

    def __init__(self):
        """
        Populates the two substitution lists
        """
        for i in range(256):
            self.s_box.append(s_box_function(i))
            self.i_box.append(inv_s_box_function(i))

    def sub(self, b):
        """
        Substitutes byte b through bitwise operations
        :param b: byte value to calculate byte substitution
        :return:
        """
        return self.s_box[b]

    def inv(self, b):
        """
        Inverts substituted byte b through bitwise operations
        :param b: byte value to be invert substitution through calculation
        :return:
        """
        return self.i_box[b]

    def subs(self, _bytes):
        """
        foreach byte loop using look-up table for byte substitution
        :param _bytes: bytearray to be iterated and substituted through look-ups
        :return: bytearray the result after substituting each byte
        """
        result = bytearray()
        for b in _bytes:
            result.append(self.sub(b))
        return result

    def sub_matrix(self, _matrix):
        result = []
        for r in _matrix:
            result.append([])
            m = self.subs(r)
            for b in m:
                result[-1].append(b)

        return result

    def inv_sub_matrix(self, _matrix):
        result = []
        for r in _matrix:
            result.append([])
            m = self.invs(r)
            for b in m:
                result[-1].append(b)

        return result

    def invs(self, _bytes):
        """
        foreach byte loop using look-up table for inverting byte substitution
        :param _bytes: bytearray to be iterated and invert substituted through look-ups
        :return: bytearray the result after invert substituting each byte
        """
        result = bytearray()
        for b in _bytes:
            result.append(self.inv(b))
        return result


"""
subs = subs_boxes()

byte = bytearray("This is a string", 'utf-8')
print(byte)

byte = subs.subs(byte)
print(byte)

byte = subs.invs(byte)
print(byte)
print(str(byte, 'utf-8'))
"""
