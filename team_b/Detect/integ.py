from myModule import kakao_send, mysql_cli, img_model, mjpg_cvlib, inout_judgment
import pymysql
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import numpy
import time

class Run:
    def __init__(self, json_infor):
        self.db_info = json_infor[:6]
        self.person_num = json_infor[6]
        self.cap = cv2.VideoCapture(json_infor[8])
        self.server = img_model.ServerSocket(json_infor[7], json_infor[9], json_infor[10])
        self.frame_path = json_infor[11]
        self.kakao = kakao_send.Kakao()

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def save_frame(self, result, frame):
        return np.max(result), frame

    def start_stop(self):#라즈베리와 소통을 시작할 시점을 결정
        try:
            ret, frame = self.cap.read()
            if ret:
                frame = mjpg_cvlib.face_detect(frame)
            return False if (type(frame) == type(None)) else True
        #(사람이 검출되지 않으면 False 검출되면 True)
        except Exception as e:
            print(str(e))
            self.start_stop()

    def convertToBinaryData(self):
        with open(self.frame_path, 'rb') as file:
            binaryData = file.read()
        return binaryData

    def detecting(self):
        roof_cnt = 0
        detect_num = 0
        past_time = 0
        detect_cnt = [0]*(len(self.person_num)-1)
        detect_acc = [0]*(len(self.person_num)-1)
        while True:
            try:
                ret, frame = self.cap.read()
                if ret:
                    frame = mjpg_cvlib.face_detect(frame)
                    if (type(frame) == type(None)): continue
                    if detect_num > 2:
                        result = self.server.model_Images(frame)
                        detect_num = 0
                    else:   
                        detect_num += 1
                        continue
            except Exception as e:
                print(str(e))
                continue

            if roof_cnt < 5:#roof_cnt가 5번 돌면 다음으로 넘어감
                print(result)
                roof_cnt += 1
                if np.max(result) > 0.85:#검출 확률이 0.7이상일때
                    if roof_cnt == 1:
                        past_result, past_frame = self.save_frame(np.max(result), frame)
                    elif np.max(result) > past_result:
                        past_result, past_frame = self.save_frame(np.max(result), frame)

                    detect_cnt[np.argmax(result)] += 1 #검출되는 인덱스 갯수 세기
                    detect_acc[np.argmax(result)] += np.max(result) #검출되는 확률 합 저장

                    if past_time == 0:  past_time = time.time()
                    elif time.time() - past_time > 3: #detecting 시간이 10초 이상 차이나면 초기화
                        detect_cnt = [0]*(len(self.person_num)-1)
                        detect_acc = [0]*(len(self.person_num)-1)
                        roof_cnt = 0
                        past_time = 0
                        print("특정시간 경과 다시 검출합니다")
                    else:   past_time = time.time()

                continue#roof_cnt가 5가 될때까지 반복

            save_frame = cv2.resize(past_frame, (70, 70), interpolation=cv2.INTER_AREA)#사진 크기 변경
            cv2.imwrite(self.frame_path, save_frame)#파일 저장
            save_frame = self.convertToBinaryData()

            print("검출완료")
            print(f"검출 확률 리스트: {detect_acc}")
            print(f"검출 인덱스별 갯수: {detect_cnt}")
            if max(detect_cnt) >= 3: #3번이상 같은 결과 또는 평균 0.7이상 나왓을때
                print("정상적으로 검출되었습니다")
                res_idx = detect_acc.index(max(detect_acc)) #확률이 가장 높은 인덱스를 구하고 저장함
                res_person = self.person_num[res_idx] #인덱스에 해당하는 사람의 연락처 저장
                res_acc = round(detect_acc[res_idx]/detect_cnt[res_idx]*100, 2) 
                #위의 인덱스에 해당하는 확률/갯수*100
            else:#그외의 확률및 미검출 결정
                print("비정상적 검출")
                res_idx = 4
                res_person = self.person_num[res_idx]
                if max(detect_acc) == 0:    res_acc = 0
                else:   res_acc = round(max(detect_acc)/detect_cnt[detect_acc.index(max(detect_acc))]*100, 2)

            print(f"검출된 사람의 인덱스: {res_idx}")
            print(f"검출된 사람의 평균 확률: {res_acc}")
            self.server.sendmessage("0")#라즈베리에 온도 요청
            print("온도 요청함")

            start_time = time.time()
            temperature = self.server.recmessage()#온도 받기
            print(f"온도를 받음: {temperature}")#받은 값을 보고 각 재보자

            temper_time = time.time()

            dicision = inout_judgment.inout(temperature, res_idx)
            #온도와 순서 따른 통과, 라즈베리파이에 보낼 신호 선출(상태, 라즈베리 신호)
            time1 = time.time()
            time2 = time.time()

            while(time2 - time1 < 1):   time2 = time.time()   

            self.server.sendmessage(dicision)#라즈베리파이에 신호 보내기
            print(f"상태를 보냄: {dicision}")
            self.kakao.send_message(res_person, temperature)#카톡에 온도가 높을때 메시지 보내기
            print("카카오 메시지 보냄")
            print(f"검출된 사람의 전화번호는 {res_person}입니다")
            
            mysql_cli.mysql_add(self.db_info, temperature, res_person, res_acc, save_frame)
            print("db에 내용 추가시킴")
            break
            #클라우드 mysql db에 내용 추가하기
        return False, temper_time-start_time
