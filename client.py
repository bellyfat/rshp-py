import socket
import time
import re
import select
import sys

HOST = '185.10.244.253'
PORT_MIN = 32766
PORT_MAX = 64000

print("Start pick sequence")
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.settimeout(0.1)

for port in range(PORT_MIN, PORT_MAX):
    print("Testing port", port)
    udp_socket.sendto(b'ping', (HOST, port))
    
    try:
        data = udp_socket.recv(1024)
    except socket.timeout:
        continue

    print(data)
    if data: break

udp_socket.close()