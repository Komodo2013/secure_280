import math

from galois_func import galois_multiply

alpha_numeric_values = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "-", "_"
]

size = 8


def xor_1d_matrices(left, right):
    result = []

    for r in range(len(left)):
        result.append(left[r] ^ right[r])

    return result


def xor_2d_matrices(__matrix1, __matrix2):
    """
    Combines two 2d lists of bytes (ints) into one by (a ^ b)
    :param __matrix1: List[ List[Int]] a 2d list holding bytes (ints)
    :param __matrix2: List[ List[Int]] a 2d list holding bytes (ints)
    :return: matrix, the resulting 2d list
    """

    # Ensure both matrices are the same size
    if len(__matrix1) != len(__matrix2) and len(__matrix2[0]) != len(__matrix1[0]):
        return

    # for each row
    for __r in range(len(__matrix1)):
        # for each column
        for __d in range(len(__matrix1[0])):
            __matrix1[__r][__d] ^= __matrix2[__r][__d]

    return __matrix1


def alpha_numeric_to_packet(string):
    n = 0x00
    for c in string:
        n = n << 6 ^ alpha_numeric_values.index(c)

    p = []
    for i in range(8):
        p.append([])
        for j in range(8):
            p.append(n & 0xff)
            n >>= 8
    return p


def string_to_packets(string):
    """
    Creates a list of 8x8 matrices of bytes representing the input
    :param string: A string of any size to be converted
    :return:
    """
    return create_packets(bytearray(string, 'utf-8'))


def create_packets(bytes_in):
    """
    Takes in a blob of bytes and divides them into a 3d list of 2d 8x8 matrices of bytes, fills by column
    :param bytes_in: a byte_array of any size
    :return: a 3d list of 2d 8x8 matrices of bytes where each matrix is defined as a packet
    """

    # Figure out how many packets we'll need
    num_packs = math.ceil(len(bytes_in) / 64)

    # iterator for the byte_array
    num_parsed = 0
    pack = [0, 0, 0, 0, 0, 0, 0, 0]
    data_packs = []
    for p in range(num_packs):
        data_packs.append(0)
        tailing_lines = 0
        remainder = []
        for row in range(8):
            to_append = []
            if num_parsed + 8 <= len(bytes_in):
                part = bytes_in[num_parsed:num_parsed + 8]
                for n in part:
                    to_append.append(n)
            else:
                if tailing_lines == 0:
                    tailing_lines += 1
                    part = bytes_in[num_parsed:]
                    for n in part:
                        remainder.append(n)
                    remainder.append(128)
                    while len(remainder) < (8 - row) * 8 - 1:
                        remainder.append(0)
                    remainder.append(7)

                    to_append = remainder[0:8]
                else:
                    to_append = remainder[tailing_lines * 8: tailing_lines * 8 + 8]
                    tailing_lines += 1
            pack[row] = to_append[:]
            num_parsed += 8
        data_packs[p] = pack[:]

    return data_packs


def packets_from_file(location):
    """
    Opens a file at location: location as a byte_array
    :param location: String the location of the file to open
    :return: 3d list of 8x8 byte matrices
    """

    # read each line of the file and copy all into one massive string
    raw = ""
    with open(location) as file:
        for line in file:
            raw += line

        # then change massive string into a bytearray
        raw_bytes = bytearray(raw, 'utf-8')

        # change bytearray into packets
    return create_packets(raw_bytes)


def packet_to_alpha_numeric(matrix):
    """
    Transforms a singe packet into an alpha_numeric representation of the value
    :param matrix: a 2d list containing ints (bytes)
    :return: String a representation of the values, 2 bits lost on a 64 byte matrix - total 510 bits represented
    """
    text = ""
    nums = []
    groups = math.floor(len(matrix) * len(matrix[0])/3)
    for group in range(groups):
        n = 0
        for i in range(3):
            n = (n << 8) ^ matrix[math.floor(group * 3 / 8)][(group * 3 + i) % 8]
        nums.append(n)

    for num in nums:
        for i in range(4):
            text += alpha_numeric_values[num & 63]
            num = num >> 6

    text += alpha_numeric_values[(matrix[-1][-1] & 252) >> 2]

    return text


def shift_rows(byte_matrix, __s__ = 8):
    """
    Shifts each row left by n spaces, where n is the index of the row. rows are defined as the nth index of each list
    :param byte_matrix: any sized 2d matrix of values
    :return: The resulting 2d list of values after shifting
    """
    __shifted_matrix = []

    # incidentally, python's .append and .set have the same operation cost....
    for __i in range(__s__):
        __shifted_matrix.append([])
        for __j in range(__s__):
            # (j + i) % len(byte_matrix[0]) is what I use to shift the column each index
            __shifted_matrix[__i].append(byte_matrix[(__j + __i) % __s__][__j])

    return __shifted_matrix


def inv_shift_rows(byte_matrix, __s__ = 8):
    """
    Shifts each row right by n spaces, where n is the index of the row. follows column major order
    This function doesn't necessarily belong here, it isn't used by hash.py but rather encryptor.py
    :param byte_matrix: any sized 2d matrix of values
    :return: The resulting 2d list of values after shifting
    """
    new_matrix = []

    # incidentally, python's .append and .set have the same operation cost....
    for i in range(__s__):
        new_matrix.append([])
        for j in range(__s__):
            # (j*3 + i) % len(byte_matrix[0]) is what I use to shift the column each index
            new_matrix[i].append(byte_matrix[(j * 7 + i) % __s__][j])

    return new_matrix


# sample 2d list of bytes (ints). This is the default internal matrix
    # the following table was constructed using digits of pi, taking 3 digits % 256
    # ie 314 % 256 = 58, 159 % 256 = 159, 265 % 256 = 9 ...
enc = (
    # [0][5] 67->66 I had to change this because with > 6x6, the inverse becomes unsolvable. By changing the lsb here,
    # I was able to adapt pi's matrix to become solvable again.
    [58, 159, 9, 102, 211, 66,  # This value right here
     78, 8],
    [82, 71, 182, 32, 163, 204, 171, 169],
    [254, 70, 97, 238, 203, 230, 13, 128],
    [116, 108, 131, 94, 35, 226, 22, 211],
    [194, 30, 214, 40, 139, 72, 230, 152],
    [197, 128, 204, 187, 58, 223, 172, 23],
    [172, 44, 80, 111, 233, 28, 154, 14],
    [193, 84, 110, 43, 196, 206, 38, 127]
)

# enc ^ -1
dec = (
    [220, 188, 146, 102, 214, 19, 3, 27],
    [29, 242, 140, 110, 208, 218, 107, 159],
    [80, 24, 33, 111, 57, 109, 171, 27],
    [95, 143, 74, 241, 192, 214, 144, 121],
    [118, 240, 214, 97, 66, 120, 220, 98],
    [241, 204, 100, 97, 153, 76, 73, 120],
    [250, 165, 76, 45, 31, 224, 73, 62],
    [43, 122, 123, 216, 2, 111, 142, 185]
)


def matrix_mult(a, b):
    m = []
    for ii in range(size):
        m.append([])
        for ll in range(size):
            m[-1].append(0)

    for k in range(size):
        for j in range(size):
            res = 0
            for i in range(size):
                res ^= galois_multiply(a[i][k], b[j][i])
            m[j][k] = res

    return m
