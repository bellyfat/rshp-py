import socket
import time
import re
import select
import sys

HOST = '185.10.244.253'

FIRST_BIND_PORT = 50000
HOLE_COUNT = 50

udp_socket_list = []

print('Punch a few holes...')
for punch in range(HOLE_COUNT):
    udp_socket_list.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
    
for udp_socket in udp_socket_list:
    udp_socket.sendto(b'punch', (HOST, 55555))

print('Wait for peer to find a hole...')
stop = False
while True:
    ready_socks,_,_ = select.select(udp_socket_list, [], [], 50) 
    for udp_socket in ready_socks:
        data, addr = udp_socket.recvfrom(1024)
        if(addr):
            print('Got Holepunch!', data) 
            
            break

    # Repunch after 50 seconds
    for udp_socket in udp_socket_list:
        udp_socket.sendto(b'punch', (HOST, 55555))