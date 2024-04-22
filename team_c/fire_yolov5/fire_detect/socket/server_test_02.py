import pickle
import socket
import struct
import cv2

host = 'localhost'
port = 5003

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('소켓 생성')

s.bind((host, port))
s.listen(10)

conn, addr = s.accept()

data = b''
payload_size = struct.calcsize("L")

while True:
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)