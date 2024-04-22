import time
import pymysql

sql = "SELECT * FROM temper ORDER BY time DESC limit 1;"
sql2 = "show status like '%Threads_connected%';"
while True:
    db = pymysql.connect(host='20.194.30.39',
                         user='fire',
                         password='0000',
                         charset='utf8',
                         db='fire_detect')
    cursor = db.cursor()
    cursor.execute(sql2)
    result = cursor.fetchall()
    for record in result:
        print(record)
        print(record[0])
        print(record[1])
        #print(record[2])
        
    db.close()

    time.sleep(60)