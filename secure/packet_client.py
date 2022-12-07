import random

import pydivert
from getmac import get_mac_address

import block_utils
import ehash
from ehash import MyHash

# Capture only TCP packets to port 80, i.e. HTTP requests.
w = pydivert.WinDivert("tcp.DstPort == 22 and tcp.PayloadLength > 0")

user = input("Username \t> ")
password = input("Password \t> ")

users = [
    {'user': 13959837315202159100914983156519879035530060834567903422178960391973410687916,
     'token': '99231904172200624786431484194345375731751515627694547872591508992352146994883'}
]

__hash = MyHash()

__hash.set_internal_matrix(user).hash_packs(ehash.string_to_packets(password), security=4)
authUUID = {"user": __hash.get_bytes() >> 256, "token": str(__hash.get_bytes() % 2**256)}
print(authUUID)

ohash = __hash.reset_internal_matrix().set_internal_matrix(authUUID["token"])

w.open()
while True:
    packet = w.recv()

    if packet.is_outbound:
        __hash.hash_packs(block_utils.create_packets(packet.payload), security=4)

        load = bytearray(packet.payload)
        load.extend(authUUID["user"].to_bytes(length=32, byteorder="big"))
        load.extend(__hash.get_bytes().to_bytes(length=64, byteorder="big"))

        packet.payload = bytes(load)

        __hash = ohash
        w.send(packet)  # re-inject the packet into the network stack

    else:
        raw = bytearray(packet.payload)
        _hash = raw[-64:]
        _usr = int(raw[-96:-65])
        _data = raw[:-97]

        remote_token = 0

        for u in users:
            if _usr == u["user"]:
                remote_token = u["token"]

        my_hash = MyHash()
        my_hash.set_internal_matrix(remote_token).hash_packs(block_utils.create_packets(bytes(_data)), security=4)
        if bytearray(my_hash.get_bytes().to_bytes(length=64, byteorder="big")) == _hash:
            packet.payload = _data
            w.send(packet)

w.close()  # stop capturing packets

