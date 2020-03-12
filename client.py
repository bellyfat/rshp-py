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

def isFirst(string):
    if '1st' in string:
        return True
    else:
        return False

# Connect to server 
server_response[0] = s.recv(1024).decode()
print('Server:', server_response[0])

server_response[1] = s.recv(1024).decode()
print('Server:', server_response[1])

peer_IP = re.findall(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", server_response[0])[0]

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
            udp_socket.sendto(b'punch', (peer_IP, service_port))

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
    start_port = 32768
    end_port = 656535
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

    if port == end_port:
        print('No hole found')
        s.close()
        sys.exit()
    
    print('Found hole. Try connecting on last 10 ports')

    for port in range(port-10, port):
        udp_socket.settimeout(1)
        print('Try port', port, 'again')
        udp_socket.sendto(b'hello', (peer_IP, port))
        data, addr = udp_socket.recvfrom(1024)
        if data:
            print('Found the hole!', addr)

s.close()
        