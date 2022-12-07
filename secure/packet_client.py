"""
Filters all traffic except packets coming from a device using port 22 and is signed with the token below.
This is symmetric authentication - Tokens are not encrypted, which would be a vulnerability in production environments"""
import pydivert

import block_utils
import ehash
from ehash import MyHash

# Capture only TCP packets to port 80, i.e. HTTP requests.
w = pydivert.WinDivert("tcp.DstPort == 22 and tcp.PayloadLength > 0")

# Get the username and password, which is needed to create your own credentials
user = input("Username \t> ")
password = input("Password \t> ")

# Credentials the remote hosts are using. All 3 blue devices use these credentials
users = [
    {'user': 13959837315202159100914983156519879035530060834567903422178960391973410687916,
     'token': '99231904172200624786431484194345375731751515627694547872591508992352146994883'}
]

# Create an instance of my custom hash object
__hash = MyHash()

# This creates the authentication token we will use... It returns a 512-bit hash, the first half being the user ID and
# the second half being the token
__hash.set_internal_matrix(user).hash_packs(ehash.string_to_packets(password), security=4)
authUUID = {"user": __hash.get_bytes() >> 256, "token": str(__hash.get_bytes() % 2**256)}

# Save a copy of the hash object with just the token included as the internal seed
ohash = __hash.reset_internal_matrix().set_internal_matrix(authUUID["token"])

w.open()
while True:
    packet = w.recv()  # Get a packet from the stack

    __hash = ohash  # Copy the original hash into our hash object to use

    if packet.is_outbound:
        # hash the contents of the packet with the token we set earlier, this effectively signs the message
        __hash.hash_packs(block_utils.create_packets(packet.payload), security=4)

        # Create the bytes for the new payload contents with user token and the hash appended
        load = bytearray(packet.payload)
        load.extend(authUUID["user"].to_bytes(length=32, byteorder="big"))
        load.extend(__hash.get_bytes().to_bytes(length=64, byteorder="big"))

        packet.payload = bytes(load)

        w.send(packet)  # re-inject the packet into the network stack

    else:
        # Separate the packet payload contents into content, user id, and signed hash
        raw = bytearray(packet.payload)
        _hash = raw[-64:]
        _usr = int(raw[-96:-65])
        _data = raw[:-97]

        # Find the remote token matching the user id sent
        remote_token = '0'
        for u in users:
            if _usr == u["user"]:
                remote_token = u["token"]

        # Create vanilla hash object - I will need a vanilla hash to test the remote token to the hash
        my_hash = MyHash()
        # Attempt to recreate the signed hash using the token that the user would have used
        my_hash.set_internal_matrix(remote_token).hash_packs(block_utils.create_packets(bytes(_data)), security=4)
        if bytearray(my_hash.get_bytes().to_bytes(length=64, byteorder="big")) == _hash:  # Test equality of hashes
            # Change the packet back to containing just the contents and re-inject it into the stack
            packet.payload = _data
            w.send(packet)

# No close as this while loop can only be terminated by ending the process
