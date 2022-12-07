"""
Filters all traffic except packets coming from a device using port 22 and is signed with the token below.
This is symmetric authentication - Tokens are not encrypted, which would be a vulnerability in production environments
"""
import pydivert

import block_utils
from ehash import MyHash

# Capture only TCP packets to port 80, i.e. HTTP requests.
w = pydivert.WinDivert("tcp.DstPort == 22 and tcp.PayloadLength > 0")

# Credentials the remote hosts are using. All 3 blue devices use these credentials
users = [
    {'user': 87262977119357710713984082997899099045171324690595122945490156632326701679174,
     'token': '65722270177093944749972834208140948720261294848657785042834118653546320988877'},
    {'user': 36955419161076888104258011732143170581407678227020289488858834643312316273983,
     'token': '89515665387915504269650702630166609222628315488512425370011779161949689383362'},
    {'user': 101095905799029070303614572356959004181486003703896465013619374431030910610972,
     'token': '16942422411336226540212041105102147750480370007771270163444281908145559560856'},
    {'user': 1487471593934321450250443486743139721947911733885716286372592914817333885985,
     'token': '61119733045738558263590398992144513630408056363549058311961615476030043500740'},
    {'user': 65754384008163472361952786370931785621996881067324904687741303482277837760287,
     'token': '71861462322187537341514894659906655462393092008174612577928088822356772168867'},
    {'user': 13959837315202159100914983156519879035530060834567903422178960391973410687916,
     'token': '99231904172200624786431484194345375731751515627694547872591508992352146994883'}
]

# Create an instance of my custom hash object
__hash = MyHash()

# This is the token the server will use... This is a vulnerability to include this data here. In production,
# This would be generated and stored on the device itself
authUUID = {'user': 13959837315202159100914983156519879035530060834567903422178960391973410687916,
            'token': '99231904172200624786431484194345375731751515627694547872591508992352146994883'}

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

        remote_token = '0'

        # Find the remote token matching the user id sent
        for u in users:
            if _usr == u["user"]:
                remote_token = u["token"]

        # Create vanilla hash object - I will need a vanilla hash to test the remote token to the hash
        my_hash = MyHash()
        # Attempt to recreate the signed hash using the token that the user would have used
        my_hash.set_internal_matrix(remote_token).hash_packs(block_utils.create_packets(bytes(_data)), security=4)
        if bytearray(my_hash.get_bytes().to_bytes(length=64, byteorder="big")) == _hash:
            # Change the packet back to containing just the contents and re-inject it into the stack
            packet.payload = _data
            w.send(packet)

# No close as this while loop can only be terminated by ending the process
