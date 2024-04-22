import threading
import time
import serial
import pymysql
import Adafruit_DHT

a = None

def temper():
    sensor = Adafruit_DHT.DHT11
    pin=18
    cur = None
    conn = pymysql.connect(host='20.194.30.39',
                       user='fire',
                       password='0000',
                       charset='utf8',
                       db='fire_detect')
    cur = conn.cursor()
    while(True):
        h, t = Adafruit_DHT.read_retry(sensor, pin)
        if (h is not None) and (t is not None) :
            tem = ("{:.1f}".format(t))
            hum = ("{:.1f}".format(h))
            sql = "INSERT INTO temper (time, temperature, humidity) VALUES (NOW(), %s, %s);"
            cur.execute(sql, (tem, hum))
            print("온도 : ", tem)
            print("습도 : ", hum)
        else:
            continue

        conn.commit()
        print('rowcount: ', cur.rowcount)
        time.sleep(1)

def readdb():
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
            print("DB시간 : ", record[0])
            print("DB불개수 : ", record[1])
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
            ser.write('s'.encode('utf-8'))
            time.sleep(0.5)
            if a == 0:
                continue

if __name__=="__main__":
    thread1 = threading.Thread(target=readdb)
    thread2 = threading.Thread(target=uart)
    thread3 = threading.Thread(target=temper)
    thread1.start()
    thread2.start()
    thread3.start()