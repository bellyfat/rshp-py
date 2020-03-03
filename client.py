import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 55555        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 12345)) 
s.connect((HOST, PORT))

data = s.recv(1024).decode()
print('Server:', repr(data))

data = s.recv(1024).decode()
print('Server:', repr(data))

