"""
This is a library of functions useful for generating hashes. Support includes hashes from files or from byte arrays.
hashes provided have the same length hash as SHA 384 after using packet_to_alpha_numeric(hash)

TODO: recreate your hash algorithm using a more AES style - sub, shift, mix, add round key from other byte
TODO: make the function more efficient, use less arrays

This hash function meets the following criteria:
- Hash is deterministic
- changing 1 bit with iterations >= 4 causes avalanche effect
- values are fairly uniform : TODO: make a test and use it on the raw bytes to see how uniform the distribution is
- somewhat efficient, the function is able to hash 55kb with iterations = 4 in 2.7s and i = 8 in 5.2s

Most useful as:
my_hash = MyHash()
my_hash.hash_packs(string_to_packets(String s), i)
my_hash.hash_packs(packets_from_file(String location), i)

To create packets:
create_packets(bytes_in)
packets_from_file(location)
string_to_packets(string)

To use the hash program:
.set_internal_matrix(String s)
.hash_packs(byte_matrices, iterations)

To convert a byte_matrix to string:
packet_to_alpha_numeric(matrix)

example:
my_hash = MyHash()
username, password = "username", "1234"
packet_to_alpha_numeric(my_hash.set_internal_matrix(username).hash_packs(string_to_packets(password), 40))

:author Jacob Larsen
:updated 20 Oct 2021

Changed the hash algorithms to be faster, more stable, and provide better distribution. Algorithm now follows a
Rijndael cipher like structure
"""

# Import used only once, for math.ceil in create_packets(bytes_in) to determine how many packets to generate
import math

# I use this to turn bytes (ints) % list length into characters, see packet_to_alpha_numeric(byte_matrix)
from crypto.subsboxes import SubsBoxes

alpha_numeric_values = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w",
    "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
]


def mix_matrices(matrix1, matrix2):
    """
    Combines two 2d lists of bytes (ints) into one through (a+b) * 31
    31 chosen as first two digits of pi
    :param matrix1: List[ List[Int]] a 2d list holding bytes (ints)
    :param matrix2: List[ List[Int]] a 2d list holding bytes (ints)
    :return: matrix, the resulting 2d list
    """

    # Ensure both matrices are the same size
    if len(matrix1) != len(matrix2) and len(matrix2[0]) != len(matrix1[0]):
        return

    # get sizes of the matrices
    rows = len(matrix1)
    columns = len(matrix1[0])

    # for each row
    for r in range(rows):
        # for each column
        for d in range(columns):
            matrix1[r][d] = (matrix1[r][d] ^ matrix2[r][d])

    return matrix1


def inv_shift_rows(byte_matrix):
    """
    Shifts each row right by n spaces, where n is the index of the row. follows column major order
    This function doesn't necessarily belong here, it isn't used by hash.py but rather encryptor.py
    :param byte_matrix: any sized 2d matrix of values
    :return: The resulting 2d list of values after shifting
    """
    new_matrix = []

    # incidentally, python's .append and .set have the same operation cost....
    for i in range(len(byte_matrix)):
        new_matrix.append([])
        for j in range(len(byte_matrix[0])):
            # (j*3 + i) % len(byte_matrix[0]) is what I use to shift the column each index
            new_matrix[i].append(byte_matrix[(j * 3 + i) % len(byte_matrix[0])][j])

    return new_matrix


def shift_rows(byte_matrix):
    """
    Shifts each row left by n spaces, where n is the index of the row. rows are defined as the nth index of each list
    :param byte_matrix: any sized 2d matrix of values
    :return: The resulting 2d list of values after shifting
    """
    new_matrix = []

    # incidentally, python's .append and .set have the same operation cost....
    for i in range(len(byte_matrix)):
        new_matrix.append([])
        for j in range(len(byte_matrix[0])):
            # (j + i) % len(byte_matrix[0]) is what I use to shift the column each index
            new_matrix[i].append(byte_matrix[(j + i) % len(byte_matrix[0])][j])

    return new_matrix


def mix_columns(byte_matrix):
    """
    Mixes each value of one sub list in an 8x8 matrix of ints. This operation is practically irreversible and is
    responsible for the security of the hash. It depends on solving x = [8 ints] where x * vector = output.
    :param byte_matrix: a 8x8 matrix of bytes (ints) to operate on
    :return: the resulting 8x8 matrix from the operation
    """

    """
    Deeper dive into the security here:
    let x = [8 ints] or one of the sub lists of the 2d list
    and v = [2, 3, 5, 7, 11, 13, 17, 19] being first 8 prime numbers 
    one must solve z = y % 256 where y = x[0] * v[0] ^ x[1] * v[1] ... ^ x[7] * v[7]
    to be able to undo this function. Given the difficulty of solving ^ without at least 2 bytes, and the use of % 256
    there should not be a more efficient method to determine z other than brute force.
    Word of caution: since one cannot prove the null, I cannot tell you there isn't a way to solve it, just I can't
    
    The only weakness I see is that a ^ ... ^ z would = 0 if each value a-z had a matching pair. the odds of this 
    happening are incredibly low... < 1e-14, as that is the chance of a single match occurring. If it did happen, then
    you still don't know which values match ie a with b? d? e? and thus cannot reverse the function 
    """
    new_matrix = [[], [], [], [], [], [], [], []]
    vector = [2, 3, 5, 7, 11, 13, 17, 19]

    for i in range(len(byte_matrix)):
        for j in range(len(byte_matrix[0])):
            val = 0
            for k in range(len(vector)):
                val = val ^ (byte_matrix[i][(j+k) % len(byte_matrix[0])] * vector[k])

            new_matrix[i].append(val % 256)

    return new_matrix


def hash_(byte_matrix, iterations):
    """
    Controller for hashing a specific byte_matrix using Rijndael cipher like combinations
    :param byte_matrix: an 8x8 matrix of bytes (ints). Must be 8x8 or out of bounds exception will be raised
    :param iterations: the number of times to repeat the process. I find iterations >= 4 to be sufficiently mixed
    :return: byte_matrix, the resulting 8x8 byte matrix
    """

    s = SubsBoxes()

    for i in range(iterations):
        # operations combined to reduce saving to byte_matrix
        byte_matrix = mix_columns(shift_rows(s.sub_matrix(byte_matrix)))
    return byte_matrix


def create_packets(bytes_in):
    """
    Takes in a blob of bytes and divides them into a 3d list of 2d 8x8 matrices of bytes, fills by column
    :param bytes_in: a byte_array of any size
    :return: a 3d list of 2d 8x8 matrices of bytes where each matrix is defined as a packet
    """

    # Figure out how many packets we'll need
    num_packs = math.ceil(len(bytes_in)/64)

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
            if num_parsed+8 <= len(bytes_in):
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
                    while len(remainder) < (8-row) * 8 - 1:
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
    TODO: we can change this to actually read in bits, 6 at a time to get more characters, as is just takes lsbits
    :param matrix: a 2d list containing ints (bytes)
    :return: String a representation of the values, 2 bits lost/ byte
    """
    text = ""
    for r in matrix:
        for c in r:
            char = alpha_numeric_values[c % len(alpha_numeric_values)]
            text += char
    return text


def string_to_packets(string):
    """
    Creates a list of 8x8 matrices of bytes representing the input
    :param string: A string of any size to be converted
    :return:
    """
    return create_packets(bytearray(string, 'utf-8'))


class MyHash:
    """
    Holds useful functions for creating hashes. More importantly, allows multiple instances with different
    internal matrices.
    """

    # sample 2d list of bytes (ints). This is the default internal matrix. generated by randInt(0,255) repeated
    # the following table was constructed using digits of pi, taking 2-3 digits so long as its < 256
    # 0's that became leading 0's were omitted, with comments locating each missing 0
    data = (
        [31, 41, 59, 26, 53, 58, 97, 93],
        [238, 46, 26, 43, 38, 32, 79, 50],
        [233, 124, 194, 224, 73, 244, 115, 27],
        [28, 84, 197, 169, 39, 93, 75, 105],
        [82, 97, 49, 44, 59, 230, 78, 164],  # second value 97 would be 097 following pi
        [62, 86, 208, 99, 86, 28, 34, 82],  # first value 62 would be 062 following pi, value 34 would be 034
        [53, 42, 117, 67, 98, 214, 80, 86],  # value 67 would be 067 following pi
        [51, 32, 82, 30, 66, 47, 93, 84]  # value 66 would be 066 following pi again
    )

    def __init__(self, internal_matrix = data):
        """
        constructor function, allows the setting of the internal_matrix upon creation
        :param internal_matrix: List[ List[Int]] 2d list of bytes (ints) to be used as the internal matrix
        """
        self.internal_matrix = []
        for i in range(len(internal_matrix)):
            self.internal_matrix.append(internal_matrix[i][:])

    def hash_packs(self, byte_matrices, iterations):
        """
        Creates a hash matrix from a list of byte matrices using iterations loops per packet
        :param byte_matrices: List [List [ List [Int] ] ] 3d list containing bytes (ints)
        :param iterations: The number of loops for each pack of bytes to run the hash algorithm
        :return: List[ List[Int]] the resulting hashed matrix
        """

        # Initialize the variable for out-of-loop access
        byte_matrix = 0
        # for each byte matrix received
        for i in range(len(byte_matrices)):
            # with first matrix, mix the internal matrix
            if i == 0:
                byte_matrix = mix_matrices(self.internal_matrix, byte_matrices[i])
            # Other iterations, mix our resulting matrix with next
            else:
                byte_matrix = mix_matrices(byte_matrix, byte_matrices[i])

            # new hash function which is more stable, runs faster, and has better distribution
            byte_matrix = hash_(byte_matrix, iterations)

        return byte_matrix

    def set_internal_matrix(self, seed):
        """
        Sets the internal matrix based of the seed provided, using the current internal matrix
        :param seed: String of any size
        :return: self for chaining
        """
        # honestly I could just decide to hash the seed..... IDK why I don't just do that......

        # get packets from the seed
        packets = string_to_packets(seed)

        self.internal_matrix = MyHash().hash_packs(packets, 5)
        return self


my_hash1 = MyHash()
my_hash2 = MyHash()
my_hash1.set_internal_matrix("2644018047581211400585215085181721409693417654472581102520728261574290329269")
my_hash2.set_internal_matrix("2644018047581211400585215085181721409693417654472581102520728261574290329269")
print(packet_to_alpha_numeric(my_hash1.internal_matrix))
print(packet_to_alpha_numeric(my_hash2.internal_matrix))

hash1 = my_hash1.hash_packs(string_to_packets("MyPass1"), 4)
hash2 = my_hash2.hash_packs(string_to_packets("MyPass2"), 4)
print(packet_to_alpha_numeric(hash1))
print(packet_to_alpha_numeric(hash2))
