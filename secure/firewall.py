"""
Scans for open ports on this device
Sets up firewall rules to block all ports except port 22 for ssh
"""
import socket
from queue import Queue
import threading
import os

timeout = 1 / 5


def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print("Port {} is open!".format(port))
            open_ports.append(port)
        else:
            print("Port {} is closed!".format(port))
            closed_ports.append(port)


def portscan(port):
    sock = socket.socket()
    sock.settimeout(timeout)
    r = sock.connect_ex((target, port))
    sock.close()
    if r == 0:
        return True
    else:
        return False


def run_scanner(threads):
    for port in range(0, 1025):
        queue.put(port)

    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()
    open_ports.sort()
    print("Open ports are:", open_ports)
    closed_ports.sort()
    print("Closed ports are:", closed_ports)


def portoc(list):
    count = 0
    if os.name == 'posix':  # install and configure firewall service for linux devices
        os.system("apt-get install ufw")
        os.system("ufw default deny incoming")
        os.system("ufw default allow outgoing")
        os.system("ufw allow ssh")
        os.system("ufw allow 22")
    elif os.name == 'nt':  # configure firewall service for windows devices
        for i in open_ports:
            if open_ports[count] != 22:
                os.system(
                    "netsh advfirewall firewall add rule name=\"Block TCP\" protocol=TCP dir=out remoteport=" + list[
                        count] + " action=block")
                os.system("netsh advfirewall firewall add rule name=\"Block UDP\" protocol=UDP dir=out remoteport=" +
                          list[count] + " action=block")


hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
target = IPAddr
queue = Queue()
open_ports = []
closed_ports = []
input = input('Please list how many threads you would like to run: ')
threads = int(input)
print("Now running scan on all TCP/UDP ports 0-1024 on your host machine using " + input + " threads")
run_scanner(threads)
portoc(open_ports)
