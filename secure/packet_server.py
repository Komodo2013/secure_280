import random

import pydivert
from getmac import get_mac_address

import block_utils
import ehash
from ehash import MyHash

# Capture only TCP packets to port 80, i.e. HTTP requests.
w = pydivert.WinDivert("tcp.DstPort == 22 and tcp.PayloadLength > 0")

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

__hash = MyHash()

authUUID = {'user': 13959837315202159100914983156519879035530060834567903422178960391973410687916,
            'token': '99231904172200624786431484194345375731751515627694547872591508992352146994883'}

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
