import os
import glob
import time
import pymysql

time.sleep(5)
 
cur = None
conn = pymysql.connect(host='20.194.30.39',
                       user='fire',
                       password='0000',
                       charset='utf8',
                       db='fire_detect')
                        
cur = conn.cursor()

dir_PATH = 'C:/yolov5-master/runs'
labels_PATH = 'C:/yolov5-master/runs/detect/exp/labels'
txt_PATH = 'C:/yolov5-master/runs/detect/exp/labels/*.txt'

fire_count = 0
non_fire_count = 0
no_txt_len = 0

def fire_num():
    global cur, conn, fire_count, non_fire_count, no_txt_len

    while(True):
        dir_list = os.listdir(dir_PATH)
        dir_count = len(dir_list)
        #print(dir_count)
        if dir_count < 1: #폴더가 없으면 아래 코드 무시 1개이상 있으면 아래 코드 실행
            continue
        
        file_list = os.listdir(labels_PATH)
        file_count = len(file_list)
        #print(file_count)
        if file_count < 1: #폴더안에 좌표값txt가 없으면 아래 코드 무시 1개이상 있으면 아래 코드 실행
            continue
        
        label_list = sorted(glob.glob(txt_PATH), key=os.path.getctime, reverse=True)
        first_list = label_list[0]
        #print(first_list)

        time.sleep(2)

        label_list2 = sorted(glob.glob(txt_PATH), key=os.path.getctime, reverse=True)
        second_list = label_list2[0]     
        #print(second_list)

        with open(first_list) as a:   #txt파일을 읽어 각 행 개수 파악
            txt_len = len(a.readlines())
            a.close()
            print('불 개수 :', txt_len)
        
        if first_list != second_list:   
            fire_count += 1 
            non_fire_count = 0
            
        else:
            non_fire_count += 1
            fire_count = 0

        print('화재 상황 카운트 : ', fire_count)
        print('화재 종료 카운트 : ', non_fire_count)
        
        if fire_count >= 3 and non_fire_count == 0:
            sql = "INSERT INTO detect (detect_time, detect_num) VALUES (NOW(), %s);"
            cur.execute(sql, (txt_len))
            print("fire")

        elif fire_count < 3 and non_fire_count < 3:
            sql = "INSERT INTO detect (detect_time, detect_num) VALUES (NOW(), %s);"
            cur.execute(sql, (no_txt_len))
            print("loading") 

        else:
            non_fire_count >= 3 and fire_count == 0
            sql = "INSERT INTO detect (detect_time, detect_num) VALUES (NOW(), %s);"
            cur.execute(sql, (no_txt_len))
            print("nofire")

        conn.commit()
        #print('rowcount: ', cur.rowcount)

if __name__== "__main__":
    fire_num()
