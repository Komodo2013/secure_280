print("""
KeepSafe 1.0

PC is for when you run this script on your own computer, and not a VM
- Please note that all other connections through port 22 will be dropped

Client is for the device that will SSH into the other boxes (presumably Kali)
- It will configure firewall rules to block all connections except on port 22
- It will allow only authenticated connections on port 22, all others will be dropped

Server is for the device that will SSH into the other boxes all others
- It will configure firewall rules to block all connections except on port 22
- It will allow only authenticated connections on port 22, all others will be dropped

Terminate the process manually when finished (the loop on port 22 is never-ending)
""")

__in = input("Server, Client, or PC?\t> ")

if "PC" in __in:
    import packet_client
elif "Client" in __in:
    import firewall
    import packet_client
else:
    import firewall
    import packet_server
