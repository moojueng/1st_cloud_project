import cv2
import sys
from PyQt5 import QtWidgets, QtGui, QtCore, QtTest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *
import time
from Module import sock_cli, temper
import os

class Thread1(QThread):
    def __init__(self, parent, label_1, mjpg_PATH):
        super().__init__(parent)
        self.label_1 = label_1
        self.mjpg_PATH = mjpg_PATH

    def run(self):
        self.show_video()

    def show_video(self):
        cap = cv2.VideoCapture(self.mjpg_PATH)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.label_1.resize(width, height)
        while True:
            ret, img = cap.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                h,w,c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                resizeImage = pixmap.scaled(600, 480, QtCore.Qt.KeepAspectRatio)
                QApplication.processEvents()
                self.label_1.setPixmap(pixmap)
            else:
                QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break
            QtTest.QTest.qWait(5)
        cap.release()
        print("Thread end.")

class Thread2(QThread):
    def __init__(self, parent, cli, label_2, temp_move):
        super().__init__(parent)
        self.cli = cli
        self.label_2 = label_2
        self.temp_move = temp_move

    def run(self):
        self.check_temp()

    def time_term(self):
        first = time.time()
        second = time.time()
        while second-first < 1.8:
            QApplication.processEvents()
            second = time.time()

    def check_temp(self):
        self.label_2.setText("대기중입니다(진행이 안될경우 고개를 움직이세요)")
        self.label_2.setFont(QtGui.QFont("궁서",38))
        self.label_2.setStyleSheet("color: black;"
                         "border-style: solid;"
                         "border-width: 5px;"
                         "border-color: #7FFFD4;"
                         "border-radius: 5px")
        while True:
            QApplication.processEvents()
            sign = self.cli.recmessage()
            if '0' in sign:
                self.label_2.setText("체온을 측정합니다(진행이 안될경우 가까이 와주세요)")
                self.label_2.setStyleSheet("color: green;"
                             "border-color: #7FFFD4;")
                tot_temp = 0.0
                for i in range(3):
                    temper = self.temp_move.get_temp()
                    tot_temp += temper
                temper = round(tot_temp / 3.0, 2)    
                temp = str(temper)
                self.cli.sendtemp(temp)

                self.label_2.setText(f"측정온도: {temp}")

                self.time_term()
                sign = self.cli.recmessage()
                if '1' in sign:
                    self.label_2.setText("등록자 / 온도정상")
                    self.label_2.setStyleSheet("color: blue;"
                                "border-color: #1E90FF;")
                elif '2' in sign:
                    self.label_2.setText("등록자 / 온도이상")
                    self.label_2.setStyleSheet("color: red;"
                                "border-color: #FA8072;")
                elif '3' in sign:
                    self.label_2.setText("미등록자 / 온도정상")
                    self.label_2.setStyleSheet("color: blue;"
                                "border-color: #1E90FF;")
                elif '4' in sign:
                    self.label_2.setText("미등록자 / 온도이상")
                    self.label_2.setStyleSheet("color: red;"
                                "border-color: #FA8072;")
                self.time_term()
                if '1' in sign or '3' in sign:
                    self.label_2.setText("정상온도로 출입을 허가합니다.")
                    self.label_2.setStyleSheet("color: green;"
                                "border-color: #7FFFD4;")      
                elif '2' in sign or '4' in sign:
                    self.label_2.setText("온도이상으로 출입을 제한합니다.")
                self.time_term()
                self.label_2.setText("검출완료, 화면에서 나가주세요")
                self.label_2.setStyleSheet("color: black;"
			        "border-color: #7FFFD4;")

                self.time_term()
                self.label_2.setText("대기중입니다(진행이 안될경우 고개를 움직이세요)")
            QtTest.QTest.qWait(300)

def start(qwid, label_1, label_2, cv2_PATH, client, temp_mo):
    th1 = Thread1(qwid, label_1, cv2_PATH)
    th2 = Thread2(qwid, client, label_2, temp_mo)
    th1.start()
    th2.start()
    print("started..")

mjpg_PATH = "http://127.0.0.1:9090/?action=stream"
server_ip = "192.168.0.23"
server_port = 59010
cli = sock_cli.ClientSocket(server_ip, server_port)
temp_move = temper.Gpio_set()

app = QtWidgets.QApplication([])
win = QtWidgets.QWidget()
vbox = QtWidgets.QVBoxLayout()
label1 = QtWidgets.QLabel()
label2 = QtWidgets.QLabel()
vbox.addWidget(label1)
vbox.addWidget(label2)
win.setLayout(vbox)
start(win, label1, label2, mjpg_PATH, cli, temp_move)
win.setWindowTitle('출입 안내 시스템')
win.showMaximized()
win.show()
sys.exit(app.exec_())
