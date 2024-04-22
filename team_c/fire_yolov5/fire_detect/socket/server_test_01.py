import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

port = 5002
host_ip = '127.0.0.1'

s.connect((host_ip, port))

s.send('서버'.encode('utf-8'))

data = s.recv(1024)
print('받은 데이터 : ', data.decode('utf-8'))