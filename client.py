import socket
import time
import re
import select
import sys

HOST = 'me.antkowiak.ddnss.de'
PORT = 2280
server = (HOST, PORT)

def is_udp_port_consistent(port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', port))
    udp_socket.sendto(b'ping', ('me.antkowiak.ddnss.de', 2280))
    data = udp_socket.recv(1024)
    udp_socket.close()
    if str(port) in data.decode():
        return True
    else:
        return False

def isFirst(string):
    if '1st' in string:
        return True
    else:
        return False

# Connect to server 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server)

response1 = s.recv(1024).decode()
print('Server:', response1)

response2 = s.recv(1024).decode()
print('Server:', response2)

peer_IP = re.findall(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", response2)[0]

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if isFirst(response1):
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
        udp_socket.sendto(b'Hello', (peer_IP, 55555))

    print('Wait for peer to find a hole...')
    stop = False
    while True:
        ready_socks,_,_ = select.select(udp_socket_list, [], [], 50) 
        for udp_socket in ready_socks:
            data, addr = udp_socket.recvfrom(1024)
            if(addr):
                print('Got Holepunch! Sending a stop signal to server') 
                s.send(b'Stop!')
                print('Waiting for second punch')
                data, addr = udp_socket.recvfrom(1024)
                print('Got second punch. Say hello')
                udp_socket.sendto(b'hello', addr)
                udp_socket.sendto(b'hello', addr)
                stop = True

        if stop:
            break

        # Repunch after 50 seconds
        for udp_socket in udp_socket_list:
            udp_socket.sendto(b'punch', (peer_IP, 55555))

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
    time.sleep(2)
    start_port = 32766
    end_port = 65536
    stop = False
    for port in range(start_port, end_port):
        ready_socks, _, _ = select.select([s], [], [], 0)
        for sock in ready_socks:
            data = sock.recv(1024)
            print('Got stop signal')
            stop = True
        if stop:
            break

        print('Try port', port)
        udp_socket.sendto(b'ping', (peer_IP, port))

    if port == end_port - 1:
        print('No hole found')
        s.close()
        sys.exit()
    
    print('Found hole. Try connecting on last 10 ports')

    for port in range(port-10, port):
        udp_socket.settimeout(2)
        print('Try port', port, 'again')
        udp_socket.sendto(b'hello', (peer_IP, port))
        try:
            data, addr = udp_socket.recvfrom(1024)
        except:
            pass
        
        if data:
            print('Found the hole!', addr)

s.close()
        