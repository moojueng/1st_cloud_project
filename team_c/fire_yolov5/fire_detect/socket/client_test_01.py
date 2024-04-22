import socket

s = socket.socket()

port = 5002
s.bind(('127.0.0.1', port))
s.listen(5)

while True:
    c, addr = s.accept()
    print('클라이언트 주소는 : ', addr)

    c.send('답장중...'.encode())

    c.close()