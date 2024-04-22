import numpy
import socket
import time
import cv2
from datetime import datetime
import sys
import base64
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model

class ServerSocket:

    def __init__(self, model, ip, port):
        self.model = model
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.socketOpen()

    def socketClose(self):
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')

    def socketOpen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client')

    def model_Images(self, frame):
        resize_frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_LANCZOS4)
        shape_frame = resize_frame.reshape(-1, 224, 224, 3)/255
        r = self.model.predict(shape_frame, batch_size = 1, verbose=1)
        res = r[0]
        return res

    def recmessage(self):
        try:
            tempo = self.recvall(self.conn, 64)
            tempo = tempo.decode('utf-8')
            tempo = float(tempo)
            return tempo
        except Exception as e:
            print(e)
            self.socketClose()
            self.socketOpen()
            self.recmessage()

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf
    
    def sendmessage(self, text):
        try:
            self.conn.sendall(text.encode('utf-8').ljust(64))
        except Exception as e:
            self.socketClose()
            self.socketOpen()
            self.sendmessage()
