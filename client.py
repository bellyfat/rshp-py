import socket
import time
import re
import select

HOST = 'me.antkowiak.ddnss.de'
PORT = 2280

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

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
peer_IP = HOST
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

    print('Punched ' + punch_count + ' holes')
    print('Wait for peer to find a hole')

    ready_socks,_,_ = select.select(udp_socket_list, [], []) 
    for udp_socket in ready_socks:
        data, addr = udp_socket.recvfrom(1024)
        if(addr):
            print('Got Holepunch! Sending a hello back')
            udp_socket.sendto(b'hello!', addr)

        udp_socket.close()

else:
    try_count = 30
    udp_socket_list = []

    for i in range(try_count):
        udp_socket_list.append(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
        udp_socket_list[i].settimeout(1)

    start_port = 32000
    end_port = 65535
    loop_number = 0
    while True:
        port = start_port
        print('Try port ' + port + '-' + (port + try_count))

        for udp_socket in udp_socket_list:
            udp_socket.sendto(b'Hello', (peer_IP, port))
            port = port + 1

        ready_socks,_,_ = select.select(udp_socket_list, [], []) 
        for udp_socket in ready_socks:
            data, addr = udp_socket.recvfrom(1024)
            if(addr):
                print('Got Holepunch!!!')
                print(addr)
        start_port = start_port + try_count + 1

    for udp_socket in udp_socket_list:
        udp_socket.close()
        