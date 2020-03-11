import socket
import time
import re
import select
import sys

HOST = 'me.antkowiak.ddnss.de'
PORT = 2280
server = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(server)

data = s.recv(1024).decode()
print('Server:', repr(data))

is_first = False
if '1st' in data:
    is_first = True

data = s.recv(1024).decode()
print('Server:', repr(data))

s.close()

# extract data from server response
peer_IP = re.findall(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", data)[0]
print('Peer IP is', peer_IP)

service_port = 51820

if is_first:
    punch_count = 25
    udp_socket_list = []

    print('Punch a few holes...')
    for punch in range(punch_count):
        udp_socket_list.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
        
    for udp_socket in udp_socket_list:
        udp_socket.sendto(b'Hello', (peer_IP, service_port))

    print('Punched', punch_count, 'holes')
    print('Wait for peer to find a hole')

    while True:
        ready_socks,_,_ = select.select(udp_socket_list, [], [], 50) 
        for udp_socket in ready_socks:
            data, addr = udp_socket.recvfrom(1024)
            if(addr):
                print('Got Holepunch! Sending a hello back') 
                udp_socket.sendto(b'hello!', addr)

            udp_socket.close()
        # Repunch after 50 seconds
        for udp_socket in udp_socket_list:
            udp_socket.sendto(b'Hello', (peer_IP, service_port))

else:
    try_count = 30
    udp_socket_list = []

    for i in range(try_count):
        udp_socket_list.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))

    port = 32000
    end_port = 65535
    loop_number = 0
    while True:
        if port == end_port:
            break

        port = start_port
        print('Try port', port, '-', (port + try_count))

        for udp_socket in udp_socket_list:
            udp_socket.sendto(b'Hello', (peer_IP, port))
            port = port + 1

        ready_socks,_,_ = select.select(udp_socket_list, [], []) 
        for udp_socket in ready_socks:
            udp_socket.settimeout(1)
            data, addr = udp_socket.recvfrom(1024)
            if(addr):
                print('Got Holepunch!!!')
                print(addr)

    for udp_socket in udp_socket_list:
        udp_socket.close()

# Connect to server 
server_response[0] = get_response()
server_response[1] = get_response()

peer_IP = ...

if isFirst(server_response[0]):
    print('Wait for peer to determine NAT type')
    data = s.recv(1024)

    if data.decode() == 'UDP port consistent':
        print('UDP port is consistent!')
        print('Give peer a second to punch a hole')
        time.sleep(1)

        print('Connect to peer')
        udp_socket.sendto((peer_IP, 55555))

        sys.exit()

    punch_count = 25
    udp_socket_list = []

    print('Punch a few holes...')
    for punch in range(punch_count):
        udp_socket_list.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
        
    for udp_socket in udp_socket_list:
        udp_socket.sendto(b'Hello', (peer_IP, service_port))

    print('Wait for peer to find a hole...')
    while True:
        ready_socks,_,_ = select.select(udp_socket_list, [], [], 50) 
        for udp_socket in ready_socks:
            data, addr = udp_socket.recvfrom(1024)
            if(addr):
                print('Got Holepunch! Sending a stop signal to server') 
                s.send(b'Stop!')

        # Repunch after 50 seconds
        for udp_socket in udp_socket_list:
            udp_socket.sendto(b'Hello', (peer_IP, service_port))

else:
    port = 55555
    if is_udp_port_consistent(port):
        print('Internal UDP port is equal to external.')
        s.send(b'UDP port consistent', server)

        print('Punch hole for pre defined port')
        udp_socket.sendto(b'punch', (peer_IP, port))

        print('Listen on pre defined port', port)
        data, addr = udp_socket.recvfrom(1024)

        print('Got connection from', addr)
        sys.exit()
    
    s.send(b'UDP port NOT consistent')
    print('NAT Router is not port consistent. Try the aggressive way...')
