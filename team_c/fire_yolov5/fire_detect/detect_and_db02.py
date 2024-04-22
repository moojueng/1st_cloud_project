import os
import glob
import time
import shutil
import cv2
import pymysql

rmfile_PATH = 'C:/yolov5-master/runs/detect'
if os.path.exists(rmfile_PATH):
    shutil.rmtree(rmfile_PATH)

rtsp_PATH = 'http://192.168.1.202:50036/?action=stream'
dir_PATH = 'C:/yolov5-master/runs'
labels_PATH = 'C:/yolov5-master/runs/detect/exp/labels'
txt_PATH = 'C:/yolov5-master/runs/detect/exp/labels/*.txt'
cv_text = 'fire'

def fire_num():
    time.sleep(10)
    conn = pymysql.connect(host='20.194.30.39', #DB 연결
                           user='fire',
                           password='0000',
                           charset='utf8',
                           db='fire_detect')         
    cur = conn.cursor() #연결한 DB와 상호작용하기 위해 cursor 객체를 생성
    
    fire_count = 0
    non_fire_count = 0
    no_txt_len = 0

    while(True):
        dir_list = os.listdir(dir_PATH) #dir_PATH폴더안에
        dir_count = len(dir_list)       #파일이 1개 이상일때 통과
        if dir_count < 1:
            continue
        else:
            pass

        file_list = os.listdir(labels_PATH) #labels_PATH 폴더안에
        file_count = len(file_list)         #txt파일 1개 이상일때 
        if file_count < 1:                  #반복문 탈출
            continue
        else:
            break

    while(True):
        try:    #txt_PATH폴더안에 txt모든 txt파일 이름은 최신 생성순으로 리스트 정렬 
            label_list = sorted(glob.glob(txt_PATH), key=os.path.getctime, reverse=True)
            first_list = label_list[0]
            time.sleep(1) #1초 동안 새로운 파일 입력 대기
            label_list2 = sorted(glob.glob(txt_PATH), key=os.path.getctime, reverse=True)
            second_list = label_list2[0]
        except: #오류 발생시 재실행
            pass
        
        with open(first_list) as a: #txt파일안에 좌표값으로 화재개수 측정
            txt_len = len(a.readlines())
            a.close()
        
        if first_list != second_list: #새로운 파일이 생성되면 fire count 증가
            fire_count += 1 
            non_fire_count = 0
            
        else: 
            non_fire_count += 1 #새로운 파일 입력이 없으면 non_fire count 증가
            fire_count = 0

        if fire_count >= 2 and non_fire_count == 0:
            sql = "INSERT INTO detect (detect_time, detect_num) VALUES (NOW(), %s);"
            cur.execute(sql, (txt_len))
            print("fire") #fire count가 2이상이면 화재 발생,화재개수 query문 생성 후 전송

        elif fire_count < 2 and non_fire_count < 2:
            sql = "INSERT INTO detect (detect_time, detect_num) VALUES (NOW(), %s);"
            cur.execute(sql, (no_txt_len))
            print("loading") #2개 count가 1이하이면 대기 상태 전송

        else:
            non_fire_count >= 2 and fire_count == 0
            sql = "INSERT INTO detect (detect_time, detect_num) VALUES (NOW(), %s);"
            cur.execute(sql, (no_txt_len))
            print("nofire") #non_fire count가 2이상이면 상황종료,0값 query문 생성 후 전송

        conn.commit() #전송한 데이터 갱신 확정
        print('DB전송카운트 : ', cur.rowcount)

def detect():
    cap = cv2.VideoCapture(rtsp_PATH) #실시간 스트리밍 서버에서 cap에 저장
    frame_W = 640 #영상 가로 사이즈 지정
    frame_H = 480 #영상 세로 사이즈 지정
    stop_count = 0
    
    while(True):
        dir_list = os.listdir(dir_PATH) #dir_PATH폴더안에
        dir_count = len(dir_list)       #파일이 1개 이상일때 통과
        if dir_count < 1:
            continue
        else:
            pass
                             
        f = open("C:/yolov5-master/runs/detect/exp/labels/_action_stream_0.txt", "w")
        f.write("0.000 0.500 0.500 1.000 1.000")
        f.close()       #빈폴더 인식 오류로 인하여 txt파일생성 후 반복문 종료
        break
        
    while(True):    #cap에 저장된 영상 프레임 하나를 계속 불러와서 Flask로 출력
        ret, frame = cap.read() #cap에 저장된 영상에서 frame 하나를 저장
        file_list2 = os.listdir(labels_PATH)
        file_count2 = len(file_list2)

        label_list = sorted(glob.glob(txt_PATH), key=os.path.getctime, reverse=True)
        first_list = label_list[0]
            #txt_PATH폴더안에 txt모든 txt파일 이름은 최신 생성순으로 리스트 정렬

        with open(first_list) as a: #좌표값 개수 파악
            txt_len = len(a.readlines())
            a.close()
        
        with open(first_list) as b:
            if txt_len == 1: #좌표값 1개
                xywh1 = b.read().splitlines()
                xywh1_1R = xywh1[0] 
            elif txt_len == 2: #좌표값 2개
                xywh2 = b.read().splitlines()
                xywh2_1R = xywh2[0]
                xywh2_2R = xywh2[1]
            elif txt_len == 3: #좌표값 3개
                xywh3 = b.read().splitlines()
                xywh3_1R = xywh3[0]
                xywh3_2R = xywh3[1]
                xywh3_3R = xywh3[2]
            elif txt_len == 4: #좌표값 4개
                xywh4 = b.read().splitlines()
                xywh4_1R = xywh4[0]
                xywh4_2R = xywh4[1]
                xywh4_3R = xywh4[2]
                xywh4_4R = xywh4[3]
            elif txt_len == 5: #좌표값 5개
                xywh5 = b.read().splitlines()
                xywh5_1R = xywh5[0]
                xywh5_2R = xywh5[1]
                xywh5_3R = xywh5[2]
                xywh5_4R = xywh5[3]
                xywh5_5R = xywh5[4]
            else:
                b.close()
                continue
            b.close()
        
        time.sleep(0.01)
        file_list3 = os.listdir(labels_PATH)
        file_count3 = len(file_list3)   #0.01초 사이에 새로운 데이터가 없으면 
        if file_count2 == file_count3:  #STOP count 증가
            stop_count += 1
        else:
            stop_count = 0

        if file_count3 > 50: 
            label_list2 = sorted(glob.glob(txt_PATH), key=os.path.getctime, reverse=True)
            rm_list = label_list2[-1]
            os.remove(rm_list)
        else:   #파일 접근 속도가 느려져서 txt파일 50개 까지 유지하기 위해 오래된 파일 삭제
            pass

        if stop_count < 50:
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
                pass
        else:
            pass

        ret, buffer = cv2.imencode('.jpg', frame)
        frame2 = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')