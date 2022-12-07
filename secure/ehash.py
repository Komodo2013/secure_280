"""
This is a library of functions useful for generating hashes from streams. Packet parser included, feed bytes
hashes provided have the same length hash as SHA-512. After using packet_to_alpha_numeric(hash), 2 bits are lost

TODO: make the function more efficient, use less arrays
TODO: update comments and variable names

This hash function meets the following criteria: TODO: update this section
- Hash is deterministic
- changing 1 bit with security >= 1 causes avalanche effect
- bits are fairly uniform : TODO: make a test.py and use it on the raw bytes to see how uniform the distribution is
- efficient, the function is able to hash 55kb with security = 1 in .14s and security = 8 in .24s
- TODO: test.py collision probability

Most useful as:
my_hash = MyHash()
my_hash.hash_packs(string_to_packets(String s), security)
my_hash.hash_packs(packets_from_file(String location), security)

To create packets:
create_packets(bytes_in)
packets_from_file(location)
string_to_packets(string)

To use the hash program:
.set_internal_matrix(String s)
.hash_packs(byte_matrices, security)

To convert a byte_matrix to string:
packet_to_alpha_numeric(matrix)

example:
my_hash = MyHash()
username, password = "username", "1234"
packet_to_alpha_numeric(my_hash.set_internal_matrix(username).hash_packs(string_to_packets(password), 8))
73ULcNw5_GaaJBkvlfReZ19MNcE2BhTMCxA7s0KwuE9Z4GUTMO7vvLBq3LATF-zRZ1OBIuWonOkqzCvzSWZkd


:author Jacob Larsen
:updated 03 Mar 2022

Changed the hash algorithms to be faster, more stable, and provide better distribution. Algorithm now follows a
Rijndael cipher like structure
Created elliptical curve structure
Improved matrix to alpha numeric to output 510 bits
"""

# I use this to turn bytes (ints) % list length into characters, see packet_to_alpha_numeric(byte_matrix)
import galois_func
from subsboxes import SubsBoxes
from block_utils import xor_2d_matrices, string_to_packets, shift_rows, packet_to_alpha_numeric

import ecc


def mix_columns(byte_matrix):
    """
    Mixes each value of one sub list in an 8x8 matrix of ints. This step is reversible if you get the matrix and this
    algorithm
    :param byte_matrix: a 8x8 matrix of bytes (ints) to operate on
    :return: the resulting 8x8 matrix from the operation
    """

    __xor_val = 0
    __length = len(byte_matrix[0])

    for i in range(len(byte_matrix)):
        for j in range(__length):
            __xor_val ^= byte_matrix[i][j]

        for j in range(__length):
            byte_matrix[i][j] = byte_matrix[i][j] ^ __xor_val

    return byte_matrix


def aes_matrix_from_matrix(bytes_in):
    """
    Mixes the matrix using the values of the matrix to find points to find on the curve
    This is the function that provides security for this hash algorithm
    :param bytes_in: a 8x8 matrix of bytes (ints) to operate on
    :return: the resulting 8x8 matrix from the operation
    """
    __gathered = 0

    for i in range(len(bytes_in)):
        __row = 0
        for j in range(len(bytes_in[i])):
            __row ^= bytes_in[i][j]

        __gathered = (__gathered << len(bytes_in[i])) ^ __row

    my_curve = ecc.Curve()
    p = my_curve.multiply_np(__gathered, my_curve.G)

    x = p.x
    byte_matrix = []

    for i in range(len(bytes_in)):
        byte_matrix.append([])
        for j in range(len(bytes_in[0])):
            byte_matrix[i].append(255 & x)

            if x > 255:
                x = p.x >> 8
            else:
                x = p.y

    return byte_matrix


def mix_columns_galois(byte_matrix):
    """
    Mixes each value of one sub list in an 8x8 matrix of ints. This operation is practically irreversible and is
    responsible for the security of the hash. It depends on solving x = [8 ints] where x * vector = output.
    :param byte_matrix: a 8x8 matrix of bytes (ints) to operate on
    :return: the resulting 8x8 matrix from the operation
    """

    new_matrix = [[], [], [], [], [], [], [], []]
    __xor_val = 0
    __length = len(byte_matrix[0])

    for i in range(len(byte_matrix)):
        for j in range(__length):
            __xor_val ^= byte_matrix[i][j]

        for j in range(__length):
            new_matrix[i].append(galois_func.galois_multiply(byte_matrix[i][j], __xor_val))  # byte_matrix[i][j] ^ __xor_val)

    return new_matrix


class MyHash:
    """
    Holds useful functions for creating hashes. More importantly, allows multiple instances with different
    internal matrices.
    """

    # I decided to use pi since it is an irrational number and provides a large number of easily verified bytes
    # I removed the decimal point to get a large int making byte operations easy
    pi = 3141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481
    data = ([], [], [], [], [], [], [], [])

    # This populates data with the most significant bytes in data[0, 0] and the least significant in data[7, 7]
    # Provides an 8x8 matrix of pseudorandom bytes
    for i in range(8):
        for j in range(8):
            data[7 - i].insert(0, pi & 255)
            pi = pi >> 8

    def __init__(self, internal_matrix=data):
        """
        constructor function, allows the setting of the internal_matrix upon creation
        :param internal_matrix: List[ List[Int]] 2d list of bytes (ints) to be used as the internal matrix
        """
        self.internal_matrix = [[], [], [], [], [], [], [], []]
        if type(internal_matrix) == str and len(internal_matrix) <= 64:
            self.set_internal_matrix(internal_matrix)
        elif type(internal_matrix) == str:
            self.reset_internal_matrix()
            raise Exception('Invalid matrix')
        elif internal_matrix == self.data:
            self.reset_internal_matrix()
        elif len(internal_matrix) < 8 or len(internal_matrix[0]) < 8:
            self.reset_internal_matrix()
            raise Exception('Invalid matrix')
        else:
            for i in range(len(internal_matrix)):
                self.internal_matrix[i] = (internal_matrix[i][:])

    def hash_packs(self, byte_matrices, security):
        """
        Creates a hash matrix from a list of byte matrices using iterations loops per packet
        :param byte_matrices: List [List [ List [Int] ] ] 3d list containing bytes (ints)
        :param security: The number of loops for each pack of bytes to run the hash algorithm
        :return: List[ List[Int]] the resulting hashed matrix
        """

        # Initialize the variables for out-of-loop access
        byte_matrix = 0
        s = SubsBoxes()
        # for each byte matrix received
        for i in range(len(byte_matrices)):
            # with first matrix, mix the internal matrix
            if i == 0:
                byte_matrix = mix_columns(shift_rows(s.sub_matrix(xor_2d_matrices(
                    self.internal_matrix, byte_matrices[i]))))
            # Other iterations, mix our resulting matrix with next
            else:
                byte_matrix = mix_columns(shift_rows(s.sub_matrix(xor_2d_matrices(
                    byte_matrix, byte_matrices[i]))))

        for i in range(security):
            byte_matrix = mix_columns_galois(shift_rows(s.sub_matrix(xor_2d_matrices(
                byte_matrix, aes_matrix_from_matrix(byte_matrix)))))

        return xor_2d_matrices(byte_matrix, aes_matrix_from_matrix(byte_matrix))

    def set_internal_matrix(self, seed):
        """
        Sets the internal matrix based of the seed provided, using the current internal matrix
        :param seed: String of any size
        :return: self for chaining
        """
        self.reset_internal_matrix()

        # get packets from the seed
        packets = string_to_packets(seed)

        self.internal_matrix = MyHash().hash_packs(packets, 4)
        return self

    def reset_internal_matrix(self):
        # I decided to use pi since it is an irrational number and provides a large number of easily verified bytes
        # I removed the decimal point to get a large int making byte operations easy
        pi = 3141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481

        # This populates data with the most significant bytes in data[0, 0] and the least significant in data[7, 7]
        # Provides an 8x8 matrix of pseudorandom bytes
        for i in range(8):
            for j in range(8):
                self.internal_matrix[7 - i].insert(0, pi & 255)
                pi = pi >> 8
        return self

    def get_bytes(self):
        ret = 0
        for c in self.internal_matrix:
            for i in c:
                ret = ret << 8 ^ i

        return ret


"""
my_hash1 = MyHash()
my_hash2 = MyHash()
"""
"""
my_hash1.set_internal_matrix("2644018047581211400585215085181721409693417654472581102520728261574290329269")
my_hash2.set_internal_matrix("2644018047581211400585215085181721409693417654472581102520728261574290329268")
print(packet_to_alpha_numeric(my_hash1.internal_matrix))
print(packet_to_alpha_numeric(my_hash2.internal_matrix))
"""
"""
my_hash1.set_internal_matrix("username")
my_hash2.set_internal_matrix("username")
print(packet_to_alpha_numeric(my_hash1.internal_matrix))
hash1 = my_hash1.hash_packs(string_to_packets("1234"), 8)
hash2 = my_hash2.hash_packs(string_to_packets("1235"), 8)
print(packet_to_alpha_numeric(hash1))
print(packet_to_alpha_numeric(hash2))
"""
"""
hash1 = my_hash1.hash_packs(packets_from_file("random_data.txt"), 0)
hash2 = my_hash1.hash_packs(packets_from_file("random_data.txt"), 0)
print(packet_to_alpha_numeric(hash1))
print(packet_to_alpha_numeric(hash2))
"""
