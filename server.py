import socket
import json

port = 55555

s = socket.socket()

s.bind(('', port))         
print("socket binded to", port)

s.listen(5)      
while True:
    print("socket is listening") 
    
    connection1, addr1 = s.accept()      
    print('Got 1st connection from', addr1) 

    connection1.sendall(b'You are the 1st (' + json.dumps(addr1).encode() + b'). Wait for peer...') 

    connection2, addr2 = s.accept() 
    print('Got 2nd connection from', addr2)

    connection2.sendall(b'You are the 2nd (' + json.dumps(addr2).encode() + b')') 

    # Inform cients about each other
    connection1.sendall(b'2nd peer: ' + json.dumps(addr2).encode())
    connection2.sendall(b'1st peer: ' + json.dumps(addr1).encode())

    print('Wait for client 2 to determine NAT type')
    data = connection2.recv(1024)
    print('Forward answer to client 1:', data.decode())
    connection1.sendall(data)
    
    if data.decode() == 'UDP port NOT consistent':
        print('Wait for stop signal from client 1')
        data = connection1.recv(1024)
        print('Got stop signal. Forward to client 2')
        connection2.sendall(b'Stop!')

    connection1.close()
    connection2.close()

s.close()
