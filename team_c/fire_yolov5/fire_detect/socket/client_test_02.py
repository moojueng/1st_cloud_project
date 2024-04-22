import pickle
import socket
import struct
import cv2
import numpy as np
import sys

rtsp_PATH = 'rtsp://192.168.0.11:8555/unicast'

cap = cv2.VideoCapture(rtsp_PATH)

clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',5003))

while True:
    ret, frame = cap.read()

    data = pickle.dumps(frame)

    message_size = struct.pack("L", len(data))

    clientsocket.sendall(message_size + data)