import time
import pymysql
import serial

ser = serial.Serial(port = '/dev/ttyAMA0',
                    baudrate = 9600,
                    timeout = 1)

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
    db.close()

    if record[1] != 0:
        ser.write('stop'.encode('utf-8'))
    elif record[1] == 0:
        ser.write('detect'.encode('utf-8'))
    else:
        continue

    time.sleep(2)