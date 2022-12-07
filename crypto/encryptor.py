# I need to have the following functions available: mix_columns, shift_rows, substitute, inv_substitute, key_scheduling
# Currently done: subsboxes.subs, subsboxes.invs, hash.shift_rows, add_round_key, key_scheduler, mix_columns,
#                 inverse_shift_columns, inverse_mix_columns, encrypt, decrypt,
#                 encrypt_bytes, decrypt_bytes, batch_key
import math
import timing

from crypto.galois import galois_multiply
from subsboxes import SubsBoxes
from hash import shift_rows, inv_shift_rows, MyHash
from secure_random import SecureRandom
from key_scheduler import KeyScheduler

s = SubsBoxes()

def add_round_key(data_matrix, key_matrix):
    """
    Use to both add and invert round key, loops through each element combining with xor
    :param data_matrix: matrix to iterate over to combine
    :param key_matrix: key matrix to iterate over to combine, must be same size as data_matrix
    :return: 2d list of values after combination
    """
    result = []

    rows = len(data_matrix)
    columns = len(data_matrix[0])

    if len(key_matrix) != rows or len(key_matrix[0]) != columns:
        raise "Error combining matrices"

    for r in range(rows):
        result.append([])
        for c in range(columns):
            result[r].append(data_matrix[r][c] ^ key_matrix[r][c])

    return result


multiplicand = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]
multiplicand_inv = [[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]


def mix_column(column):
    result = [0, 0, 0, 0]
    for i in range(4):
        item = 0
        for j in range(4):
            item ^= galois_multiply(column[j], multiplicand[i][j])
        result[i] = item

    return result


def inv_mix(column):
    result = [0, 0, 0, 0]
    for i in range(4):
        item = 0
        for j in range(4):
            item ^= galois_multiply(column[j], multiplicand_inv[i][j])
        result[i] = item

    return result


def mix_columns(matrix):
    result = []
    for i in range(4):
        result.append(mix_column(matrix[i])[:])
    return result


def inv_mix_columns(matrix):
    result = []
    for i in range(4):
        result.append(inv_mix(matrix[i])[:])
    return result


def encrypt(matrix, batch_key, i):
    k = KeyScheduler(batch_key).generate_keys(i + 1)
    result = []
    for m in matrix:
        result.append(m[:])

    result = k.add_key(result, 0)
    for j in range(i - 2):
        result = k.add_key(mix_columns(shift_rows(s.sub_matrix(result))), j + 1)

    result = k.add_key(shift_rows(s.sub_matrix(result)), i-1)

    return result


def decrypt(matrix, batch_key, i):
    k = KeyScheduler(batch_key).generate_keys(i)
    result = []
    for m in matrix:
        result.append(m[:])

    result = s.inv_sub_matrix(inv_shift_rows(k.add_key(result, i-1)))

    for j in range(i - 2):
        result = s.inv_sub_matrix(inv_shift_rows(inv_mix_columns(k.add_key(result, i - j - 2))))

    return k.add_key(result, 0)

def make_packets(bytes_in):
    num_bytes = len(bytes_in) - 1

    # Figure out how many packets we'll need for 4x4 matrices of bytes
    num_packs = math.ceil(num_bytes/16)

    packs = []

    for p in range(num_packs):
        packs.append([])
        for i in range(4):
            v = p * 16 + (i + 1) * 4
            if v <= num_bytes:
                packs[-1].append(bytes_in[v - 4: v])
            elif v - 4 <= num_bytes:
                packs[-1].append([])
                for j in range(4):
                    if v + j - 4 <= num_bytes:
                        packs[-1][-1].append(bytes_in[v + j - 4])
                    else:
                        packs[-1][-1].append(0)
            else:
                packs[-1].append([0, 0, 0, 0])

    return packs





class Encryptor:

    def __init__(self, key):
        key_hash = MyHash().set_internal_matrix(key).internal_matrix
        self.rand = SecureRandom(key_hash, is_packet=True)

    def get_batch_key(self):
        combination = self.rand.hasher.internal_matrix[0][:]
        for b in self.rand.hasher.internal_matrix[1]:
            combination.append(b)
        _batch = bytearray(combination)
        self.rand.addSalt()
        return _batch

    def encrypt_file(self, bytes):
        print("--making packets")
        packets = make_packets(bytes)
        results = bytearray()

        print("--encrypting packets")
        for i in range(len(packets)):
            packets[i] = encrypt(packets[i], self.get_batch_key(), 12)

        print("--transforming data")
        for p in packets:
            for r in p:
                for b in r:
                    results.append(b)

        return results

    def decrypt_file(self, bytes):
        print("--making packets")
        packets = make_packets(bytes)
        results = bytearray()

        print("--decrypting packets")
        for i in range(len(packets)):
            packets[i] = decrypt(packets[i], self.get_batch_key(), 12)

        print("--transforming data")
        for p in packets:
            for r in p:
                for b in r:
                    results.append(b)

        return results


"""
e = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
a = [[0, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
my_batch_key = bytearray("This should be 1", 'utf-8')
my_batch_key2 = bytearray("This should be 2", 'utf-8')
s = SubsBoxes()

rounds = 12
d = encrypt(e, my_batch_key, rounds)
g = encrypt(a, my_batch_key, rounds)
f = decrypt(d, my_batch_key, rounds)
h = decrypt(g, my_batch_key, rounds)

print(e)
print("-"*20)
print(d)
print(g)
print("-"*20)
print(f)
print(h)
"""


my_enc = Encryptor("1234")
my_dec = Encryptor("1234")
raw = ""
raw_bytes = bytearray()
print("Loading file")
with open("random_data.txt", "rb") as file:
    for line in file:
        raw += line

    # then change massive string into a bytearray
    raw_bytes = bytearray(raw)

    # change bytearray into packets
print("encrypting file")
encryption = my_enc.encrypt_file(raw_bytes)
print("decrypting file")
decryption = my_dec.decrypt_file(raw_bytes)

print("writing encryption")
with open('encrypted.txt', 'wb') as file:
    file.write(encryption)

#print("writing decryption")
#with open('decrypted.txt', 'w') as file:
#    file.write(str(decryption, 'utf-8'))

""""""
