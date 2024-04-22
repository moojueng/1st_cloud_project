import time
import pymysql
import serial
import threading

a = None

def db():
    global a
    sql = "SELECT * FROM detect ORDER BY detect_time DESC limit 1;"
    while True:
        db = pymysql.connect(host='20.194.30.39',
                            user='fire',
                            password='0000',
                            charset='utf8',
                            db='fire_detect')
        cursor = db.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        for record in result:
            print(record[0])
            print(record[1])
        a = record[1]
        db.close()
        time.sleep(1)

def uart():
    global a
    stop = 10
    ser = serial.Serial(port = '/dev/ttyAMA0',
                    baudrate = 9600,
                    timeout = 1)
    
    while True:
        if a == 0:
                ser.write('e'.encode('utf-8'))
                time.sleep(stop)
                if a != 0:
                    continue

                ser.write('w'.encode('utf-8'))
                time.sleep(stop)
                if a != 0:
                    continue

                ser.write('q'.encode('utf-8'))
                time.sleep(stop)
                if a != 0:
                    continue

                ser.write('w'.encode('utf-8'))
                time.sleep(stop)
                if a != 0:
                    continue

                ser.write('e'.encode('utf-8'))
                time.sleep(stop)
                if a != 0:
                    continue

                ser.write('r'.encode('utf-8'))
                time.sleep(stop)
                if a != 0:
                    continue

                ser.write('t'.encode('utf-8'))
                time.sleep(stop)
                if a != 0:
                    continue

                ser.write('r'.encode('utf-8'))
                time.sleep(stop)
                if a != 0:
                    continue
        else:
            continue

if __name__=="__main__":
    thread1 = threading.Thread(target=db) 
    thread2 = threading.Thread(target=uart) 
    thread1.start() 
    thread2.start() 