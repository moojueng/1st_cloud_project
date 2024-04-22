import socket
import sys
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 50035

server_socket.connect((host, port))

while True:
    data = server_socket.recv(1024)
    print('받은 데이터 : ', data.decode('utf-8'))
    time.sleep(1)