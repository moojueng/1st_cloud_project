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
loading = 'waiting to be detected'

cap = cv2.VideoCapture(rtsp_PATH)
frame_W = 640
frame_H = 480
stop_count = 0

cur = None
conn = pymysql.connect(host='20.194.30.39',
                       user='fire',
                       password='0000',
                       charset='utf8',
                       db='fire_detect')           
cur = conn.cursor()

fire_count = 0
non_fire_count = 0
no_txt_len = 0

def fire_num():
    global cur, conn, fire_count, non_fire_count, no_txt_len
    time.sleep(10)
    while(True):
        dir_list = os.listdir(dir_PATH)
        dir_count = len(dir_list)
        if dir_count < 1:
            continue
        
        file_list = os.listdir(labels_PATH)
        file_count = len(file_list)
        if file_count < 1:
            continue
        
        label_list = sorted(glob.glob(txt_PATH), key=os.path.getctime, reverse=True)
        first_list = label_list[0]
        time.sleep(1)
        label_list2 = sorted(glob.glob(txt_PATH), key=os.path.getctime, reverse=True)
        second_list = label_list2[0]     
        
        with open(first_list) as a:   
            txt_len = len(a.readlines())
            a.close()
        
        if first_list != second_list:   
            fire_count += 1 
            non_fire_count = 0
            
        else:
            non_fire_count += 1
            fire_count = 0

        if fire_count >= 2 and non_fire_count == 0:
            sql = "INSERT INTO detect (detect_time, detect_num) VALUES (NOW(), %s);"
            cur.execute(sql, (txt_len))
            print("fire")

        elif fire_count < 2 and non_fire_count < 2:
            sql = "INSERT INTO detect (detect_time, detect_num) VALUES (NOW(), %s);"
            cur.execute(sql, (no_txt_len))
            print("loading") 

        else:
            non_fire_count >= 2 and fire_count == 0
            sql = "INSERT INTO detect (detect_time, detect_num) VALUES (NOW(), %s);"
            cur.execute(sql, (no_txt_len))
            print("nofire")

        conn.commit()
        print('DB전송카운트 : ', cur.rowcount)

def detect():
    global cap, frame_H, frame_W, stop_count
    while(True):
        dir_list = os.listdir(dir_PATH)
        dir_count = len(dir_list)
        if dir_count < 1:
            continue

        f = open("C:/yolov5-master/runs/detect/exp/labels/_action_stream_0.txt", "w")
        f.write("0.000 0.500 0.500 1.000 1.000")
        f.close()

        file_list = os.listdir(labels_PATH)
        file_count = len(file_list)
        if file_count < 1:
            continue
        else:
            break

    while(True):
        ret, frame = cap.read()
        file_list2 = os.listdir(labels_PATH)
        file_count2 = len(file_list2)

        label_list = sorted(glob.glob(txt_PATH), key=os.path.getctime, reverse=True)
        first_list = label_list[0]

        with open(first_list) as a:
            txt_len = len(a.readlines())
            a.close()
        
        with open(first_list) as b:
            if txt_len == 1:
                xywh1 = b.read().splitlines()
                xywh1_1R = xywh1[0]
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
        
        time.sleep(0.01)
        file_list3 = os.listdir(labels_PATH)
        file_count3 = len(file_list3)
        if file_count2 == file_count3:
            stop_count += 1
        else:
            stop_count = 0

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