import socket
import cv2
import numpy
import sys
from datetime import datetime
import base64
import os
import glob
from rmfile import *

dir_PATH = 'C:/yolov5-master/runs'
labels_PATH = 'C:/yolov5-master/runs/detect/exp/labels'
txt_PATH = 'C:/yolov5-master/runs/detect/exp/labels/*.txt'
cv_text = 'fire'
loading = 'waiting to be detected'

class ClientVideoSocket:
    def __init__(self, ip, port, video_path):
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.video_path = video_path
        self.connectCount = 0
        self.connectServer()

    def connectServer(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_PORT: ' + str(self.TCP_SERVER_PORT) + ' ]')
            self.connectCount = 0
            self.sendImages()
        except Exception as e:
            print(e)
            self.connectCount += 1
            if self.connectCount == 10:
                print(u'Connect fail %d times. exit program'%(self.connectCount))
                sys.exit()
            print(u'%d times try to connect with server'%(self.connectCount))
            time.sleep(1)
            self.connectServer()

    def sendImages(self):
        frame_W = 640
        frame_H = 480
        cnt = 0
        stop_count = 0
        capture = cv2.VideoCapture(self.video_path)
        try:
            while(True):
                dir_list = os.listdir(dir_PATH)
                dir_count = len(dir_list)
                if dir_count == 0: #폴더가 없으면 아래 코드 무시 1개이상 있으면 아래 코드 실행
                    continue
                
                file_list = os.listdir(labels_PATH)
                file_count = len(file_list)
                if file_count < 6: #폴더안에 좌표값txt가 없으면 아래 코드 무시 1개이상 있으면 아래 코드 실행
                    continue
                
                label_list = sorted(glob.glob(txt_PATH), key=os.path.getctime, reverse=True)
                first_list = label_list[0] #label폴더에서 마지막생성 좌표 경로 리스트 저장
                
                with open(first_list) as a:   #txt파일을 읽어 각 행 개수 파악
                    txt_len = len(a.readlines())
                    a.close()
                
                with open(first_list) as b: #txt파일을 읽어 각 행 좌표를 리스트에 저장
                    if txt_len == 1:
                        xywh1 = b.read().splitlines()
                        xywh1_1R = xywh1[0]
                        # print(xywh1_1R)
                        # print(xywh1_1R[6:11])
                        # print(xywh1_1R[12:17])
                        # print(xywh1_1R[18:23])
                        # print(xywh1_1R[24:29])
                        # print(float(xywh1_1R[6:11])*frame_H)
                        # print(int((float(xywh1_1R[6:11])*frame_W)-((float(xywh1_1R[18:23])/2)*frame_W)))
                    elif txt_len == 2:
                        xywh2 = b.read().splitlines()
                        xywh2_1R = xywh2[0]
                        xywh2_2R = xywh2[1]
                    elif txt_len == 3:
                        xywh3 = b.read().splitlines()
                        xywh3_1R = xywh3[0]
                        xywh3_2R = xywh3[1]
                        xywh3_3R = xywh3[2]
                    elif txt_len == 4:
                        xywh4 = b.read().splitlines()
                        xywh4_1R = xywh4[0]
                        xywh4_2R = xywh4[1]
                        xywh4_3R = xywh4[2]
                        xywh4_4R = xywh4[3]
                    elif txt_len == 5:
                        xywh5 = b.read().splitlines()
                        xywh5_1R = xywh5[0]
                        xywh5_2R = xywh5[1]
                        xywh5_3R = xywh5[2]
                        xywh5_4R = xywh5[3]
                        xywh5_5R = xywh5[4]
                    else:
                        continue
                    b.close()
                
                time.sleep(0.1)
                file_list2 = os.listdir(labels_PATH)
                file_count2 = len(file_list2)
                if file_count == file_count2:
                    stop_count += 1
                else:
                    stop_count = 0

                ret, frame = capture.read()

                if stop_count < 10:
                    if txt_len == 1:
                        cv2.rectangle(frame, 
                        (int((float(xywh1_1R[6:11])*frame_W)-((float(xywh1_1R[18:23])/2)*frame_W)),
                        int((float(xywh1_1R[12:17])*frame_H)-((float(xywh1_1R[24:29])/2)*frame_H)),
                        int((float(xywh1_1R[18:23]))*frame_W),
                        int((float(xywh1_1R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh1_1R[6:11])*frame_W)-((float(xywh1_1R[18:23])/2)*frame_W)),
                        int((float(xywh1_1R[12:17])*frame_H)-((float(xywh1_1R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                    elif txt_len == 2:
                        cv2.rectangle(frame, 
                        (int((float(xywh2_1R[6:11])*frame_W)-((float(xywh2_1R[18:23])/2)*frame_W)),
                        int((float(xywh2_1R[12:17])*frame_H)-((float(xywh2_1R[24:29])/2)*frame_H)),
                        int((float(xywh2_1R[18:23]))*frame_W),
                        int((float(xywh2_1R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh2_1R[6:11])*frame_W)-((float(xywh2_1R[18:23])/2)*frame_W)),
                        int((float(xywh2_1R[12:17])*frame_H)-((float(xywh2_1R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                        cv2.rectangle(frame, 
                        (int((float(xywh2_2R[6:11])*frame_W)-((float(xywh2_2R[18:23])/2)*frame_W)),
                        int((float(xywh2_2R[12:17])*frame_H)-((float(xywh2_2R[24:29])/2)*frame_H)),
                        int((float(xywh2_2R[18:23]))*frame_W),
                        int((float(xywh2_2R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh2_2R[6:11])*frame_W)-((float(xywh2_2R[18:23])/2)*frame_W)),
                        int((float(xywh2_2R[12:17])*frame_H)-((float(xywh2_2R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                    elif txt_len == 3:
                        cv2.rectangle(frame, 
                        (int((float(xywh3_1R[6:11])*frame_W)-((float(xywh3_1R[18:23])/2)*frame_W)),
                        int((float(xywh3_1R[12:17])*frame_H)-((float(xywh3_1R[24:29])/2)*frame_H)),
                        int((float(xywh3_1R[18:23]))*frame_W),
                        int((float(xywh3_1R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh3_1R[6:11])*frame_W)-((float(xywh3_1R[18:23])/2)*frame_W)),
                        int((float(xywh3_1R[12:17])*frame_H)-((float(xywh3_1R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                        cv2.rectangle(frame, 
                        (int((float(xywh3_2R[6:11])*frame_W)-((float(xywh3_2R[18:23])/2)*frame_W)),
                        int((float(xywh3_2R[12:17])*frame_H)-((float(xywh3_2R[24:29])/2)*frame_H)),
                        int((float(xywh3_2R[18:23]))*frame_W),
                        int((float(xywh3_2R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh3_2R[6:11])*frame_W)-((float(xywh3_2R[18:23])/2)*frame_W)),
                        int((float(xywh3_2R[12:17])*frame_H)-((float(xywh3_2R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                        cv2.rectangle(frame, 
                        (int((float(xywh3_3R[6:11])*frame_W)-((float(xywh3_3R[18:23])/2)*frame_W)),
                        int((float(xywh3_3R[12:17])*frame_H)-((float(xywh3_3R[24:29])/2)*frame_H)),
                        int((float(xywh3_3R[18:23]))*frame_W),
                        int((float(xywh3_3R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh3_3R[6:11])*frame_W)-((float(xywh3_3R[18:23])/2)*frame_W)),
                        int((float(xywh3_3R[12:17])*frame_H)-((float(xywh3_3R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                    elif txt_len == 4:
                        cv2.rectangle(frame, 
                        (int((float(xywh4_1R[6:11])*frame_W)-((float(xywh4_1R[18:23])/2)*frame_W)),
                        int((float(xywh4_1R[12:17])*frame_H)-((float(xywh4_1R[24:29])/2)*frame_H)),
                        int((float(xywh4_1R[18:23]))*frame_W),
                        int((float(xywh4_1R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh4_1R[6:11])*frame_W)-((float(xywh4_1R[18:23])/2)*frame_W)),
                        int((float(xywh4_1R[12:17])*frame_H)-((float(xywh4_1R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                        cv2.rectangle(frame, 
                        (int((float(xywh4_2R[6:11])*frame_W)-((float(xywh4_2R[18:23])/2)*frame_W)),
                        int((float(xywh4_2R[12:17])*frame_H)-((float(xywh4_2R[24:29])/2)*frame_H)),
                        int((float(xywh4_2R[18:23]))*frame_W),
                        int((float(xywh4_2R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh4_2R[6:11])*frame_W)-((float(xywh4_2R[18:23])/2)*frame_W)),
                        int((float(xywh4_2R[12:17])*frame_H)-((float(xywh4_2R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                        cv2.rectangle(frame, 
                        (int((float(xywh4_3R[6:11])*frame_W)-((float(xywh4_3R[18:23])/2)*frame_W)),
                        int((float(xywh4_3R[12:17])*frame_H)-((float(xywh4_3R[24:29])/2)*frame_H)),
                        int((float(xywh4_3R[18:23]))*frame_W),
                        int((float(xywh4_3R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh4_3R[6:11])*frame_W)-((float(xywh4_3R[18:23])/2)*frame_W)),
                        int((float(xywh4_3R[12:17])*frame_H)-((float(xywh4_3R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                        cv2.rectangle(frame, 
                        (int((float(xywh4_4R[6:11])*frame_W)-((float(xywh4_4R[18:23])/2)*frame_W)),
                        int((float(xywh4_4R[12:17])*frame_H)-((float(xywh4_4R[24:29])/2)*frame_H)),
                        int((float(xywh4_4R[18:23]))*frame_W),
                        int((float(xywh4_4R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh4_4R[6:11])*frame_W)-((float(xywh4_4R[18:23])/2)*frame_W)),
                        int((float(xywh4_4R[12:17])*frame_H)-((float(xywh4_4R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)
                    
                    elif txt_len == 5:
                        cv2.rectangle(frame, 
                        (int((float(xywh5_1R[6:11])*frame_W)-((float(xywh5_1R[18:23])/2)*frame_W)),
                        int((float(xywh5_1R[12:17])*frame_H)-((float(xywh5_1R[24:29])/2)*frame_H)),
                        int((float(xywh5_1R[18:23]))*frame_W),
                        int((float(xywh5_1R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh5_1R[6:11])*frame_W)-((float(xywh5_1R[18:23])/2)*frame_W)),
                        int((float(xywh5_1R[12:17])*frame_H)-((float(xywh5_1R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                        cv2.rectangle(frame, 
                        (int((float(xywh5_2R[6:11])*frame_W)-((float(xywh5_2R[18:23])/2)*frame_W)),
                        int((float(xywh5_2R[12:17])*frame_H)-((float(xywh5_2R[24:29])/2)*frame_H)),
                        int((float(xywh5_2R[18:23]))*frame_W),
                        int((float(xywh5_2R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh5_2R[6:11])*frame_W)-((float(xywh5_2R[18:23])/2)*frame_W)),
                        int((float(xywh5_2R[12:17])*frame_H)-((float(xywh5_2R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                        cv2.rectangle(frame, 
                        (int((float(xywh5_3R[6:11])*frame_W)-((float(xywh5_3R[18:23])/2)*frame_W)),
                        int((float(xywh5_3R[12:17])*frame_H)-((float(xywh5_3R[24:29])/2)*frame_H)),
                        int((float(xywh5_3R[18:23]))*frame_W),
                        int((float(xywh5_3R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh5_3R[6:11])*frame_W)-((float(xywh5_3R[18:23])/2)*frame_W)),
                        int((float(xywh5_3R[12:17])*frame_H)-((float(xywh5_3R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                        cv2.rectangle(frame, 
                        (int((float(xywh5_4R[6:11])*frame_W)-((float(xywh5_4R[18:23])/2)*frame_W)),
                        int((float(xywh5_4R[12:17])*frame_H)-((float(xywh5_4R[24:29])/2)*frame_H)),
                        int((float(xywh5_4R[18:23]))*frame_W),
                        int((float(xywh5_4R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh5_4R[6:11])*frame_W)-((float(xywh5_4R[18:23])/2)*frame_W)),
                        int((float(xywh5_4R[12:17])*frame_H)-((float(xywh5_4R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)

                        cv2.rectangle(frame, 
                        (int((float(xywh5_5R[6:11])*frame_W)-((float(xywh5_5R[18:23])/2)*frame_W)),
                        int((float(xywh5_5R[12:17])*frame_H)-((float(xywh5_5R[24:29])/2)*frame_H)),
                        int((float(xywh5_5R[18:23]))*frame_W),
                        int((float(xywh5_5R[24:29]))*frame_H)),
                        (0,0,255), 2)
                        cv2.putText(frame, cv_text,
                        (int((float(xywh5_5R[6:11])*frame_W)-((float(xywh5_5R[18:23])/2)*frame_W)),
                        int((float(xywh5_5R[12:17])*frame_H)-((float(xywh5_5R[24:29])/2)*frame_H))), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2, cv2.LINE_AA)
                    else:
                        cv2.rectangle(frame, (0, 0), (640, 480), (0, 255, 0), 3)
                        cv2.putText(frame, loading, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 255, 0), 2, cv2.LINE_AA)

                elif stop_count > 10:
                    cv2.rectangle(frame, (0, 0), (640, 480), (0, 255, 0), 3)
                    cv2.putText(frame, loading, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 255, 0), 2, cv2.LINE_AA)
                else:
                    cv2.rectangle(frame, (0, 0), (640, 480), (0, 255, 0), 3)
                    cv2.putText(frame, loading, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 255, 0), 2, cv2.LINE_AA)
                
                now = time.localtime()
                stime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
                result, imgencode = cv2.imencode('.jpg', frame, encode_param)
                data = numpy.array(imgencode)
                stringData = base64.b64encode(data)
                length = str(len(stringData))
                self.sock.sendall(length.encode('utf-8').ljust(64))
                self.sock.send(stringData)
                self.sock.send(stime.encode('utf-8').ljust(64))
                print(u'send images %d'%(cnt))
                cnt+=1
                # cv2.imshow("fire_detect_video", frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
                time.sleep(0.01)
        except Exception as e:
            print(e)
            self.sock.close()
            time.sleep(1)
            self.connectServer()
            self.sendImages()

def main():
    TCP_IP = 'localhost'
    TCP_PORT = 50055
    video_path = 'http://192.168.1.202:50036/?action=stream'
    client = ClientVideoSocket(TCP_IP, TCP_PORT, video_path)

if __name__ == "__main__":
    main()