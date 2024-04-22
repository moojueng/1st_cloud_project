import time
import pymysql
import serial
from queue import LifoQueue 
import threading

def db(q):
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
        q.put(record[1])
        db.close()

def uart(q):
    stop = 2
    commend = ['q', 'w', 'e', 'r', 't']
    commendnum = None

    ser = serial.Serial(port = '/dev/ttyAMA0',
                    baudrate = 9600,
                    timeout = 1)
    
    while True:
        if q.get() == 0:
                ser.write('e'.encode('utf-8'))
                commendnum = 2
                if q.get() != 0:
                    break
                time.sleep(stop)

                ser.write('w'.encode('utf-8'))
                commendnum = 1
                if q.get() != 0:
                    break
                time.sleep(stop)

                ser.write('q'.encode('utf-8'))
                commendnum = 0
                if q.get() != 0:
                    break
                time.sleep(stop)

                ser.write('w'.encode('utf-8'))
                commendnum = 1
                if q.get() != 0:
                    break
                time.sleep(stop)

                ser.write('e'.encode('utf-8'))
                commendnum = 2
                if q.get() != 0:
                    break
                time.sleep(stop)

                ser.write('r'.encode('utf-8'))
                commendnum = 3
                if q.get() != 0:
                    break
                time.sleep(stop)

                ser.write('t'.encode('utf-8'))
                commendnum = 4
                if q.get() != 0:
                    break
                time.sleep(stop)

                ser.write('r'.encode('utf-8'))
                commendnum = 3
                if q.get() != 0:
                    break
                time.sleep(stop)

        else:
            ser.write(commend[commendnum].encode('utf-8'))

if __name__=="__main__":
    q = LifoQueue()
    thread1 = threading.Thread(target=db, args=(q, )) 
    thread2 = threading.Thread(target=uart, args=(q, )) 
    thread1.start() 
    thread2.start() 
    thread1.join() 
    thread2.join()