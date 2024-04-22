import socket
import os
import glob
import time

fire_count = 0
non_fire_count = 0

dir_PATH = 'C:/yolov5-master/runs'
labels_PATH = 'C:/yolov5-master/runs/detect/exp/labels'
txt_PATH = 'C:/yolov5-master/runs/detect/exp/labels/*.txt'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = 'localhost'
port = 50035

client_socket.bind((host, port))
client_socket.listen(5)
client_socket, addr = client_socket.accept()
print('Connected by', addr)

while True:
    dir_list = os.listdir(dir_PATH)
    dir_count = len(dir_list)
    #print(dir_count)
    if dir_count == 0: #폴더가 없으면 아래 코드 무시 1개이상 있으면 아래 코드 실행
        continue
    
    file_list = os.listdir(labels_PATH)
    file_count = len(file_list)
    #print(file_count)
    if file_count == 0: #폴더안에 좌표값txt가 없으면 아래 코드 무시 1개이상 있으면 아래 코드 실행
        continue
    
    label_list = sorted(glob.glob(txt_PATH), key=os.path.getctime, reverse=True)
    first_list = label_list[0]
    time.sleep(3)
    second_list = label_list[0]     
    print(first_list)
    print(second_list)
    
    if first_list != second_list:   
        fire_count += 1 
        non_fire_count = 0
        print(fire_count)
        print(non_fire_count)
        print('\n')
    else: 
        fire_count == second_list
        non_fire_count += 1
        fire_count = 0
        print(fire_count)
        print(non_fire_count)
        print('\n')
    
    if fire_count >= 3 and non_fire_count == 0:
        print("화재 발생!!")
        client_socket.send('fire'.encode())
    elif fire_count < 3 and non_fire_count < 3:
        print("상황파악중") 
        client_socket.send('Loading'.encode())
    else:
        non_fire_count >= 3 and fire_count == 0
        print("화재 상황 종료")
        client_socket.send('non_fire'.encode())





