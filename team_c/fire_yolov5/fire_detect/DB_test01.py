import os
import glob
import time
import pymysql

time.sleep(5)

# 전역변수 선언부 
db = None 
cur = None

conn = pymysql.connect(host='20.39.201.16',
                       user='fire',
                       password='0000',
                       charset='utf8',
                       db='fire_detect') #DB 연결
                        
cur = conn.cursor() #연결한 DB와 상호작용하기 위해 cursor 객체를 생성

dir_PATH = 'C:/yolov5-master/runs'
labels_PATH = 'C:/yolov5-master/runs/detect/exp/labels'
txt_PATH = 'C:/yolov5-master/runs/detect/exp/labels/*.txt'

fire_count = 0
non_fire_count = 0

no_txt_len = 0

fire = "fire"
loading = "loading"
non_fire = "non_fire"


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
    
    if first_list != second_list:   
        fire_count += 1 
        non_fire_count = 0
        
    else:
        non_fire_count += 1
        fire_count = 0

    print(fire_count)
    print(non_fire_count)
    
    if fire_count >= 3 and non_fire_count == 0:
        sql = "INSERT INTO detect_table (state, detect_num, detect_time) VALUES (%s, %s, NOW());"
        cur.execute(sql, (fire, txt_len))
        print("화재 발생!!")

    elif fire_count < 3 and non_fire_count < 3:
        sql = "INSERT INTO detect_table (state, detect_num, detect_time) VALUES (%s, %s, NOW());"
        cur.execute(sql, (loading, no_txt_len))
        print("상황파악중") 

    else:
        non_fire_count >= 3 and fire_count == 0
        sql = "INSERT INTO detect_table (state, detect_num, detect_time) VALUES (%s, %s, NOW());"
        cur.execute(sql, (non_fire, no_txt_len))
        print("화재 상황 종료")

    conn.commit()
    print('rowcount: ', cur.rowcount)
