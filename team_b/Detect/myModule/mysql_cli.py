import pymysql

def mysql_add(db_info, temp, person_num, accuracy, frame):
    db = pymysql.connect(host = db_info[0], port=db_info[1], user=db_info[2], passwd=db_info[3], db=db_info[4], charset=db_info[5])
    cursor = db.cursor(pymysql.cursors.DictCursor)
    if person_num != '-':
        sql = "INSERT INTO electronic_list (Date, Time, phone_num, person_name, addr, sex, temperature, accuracy, img) select now(), now(), phone_num, person_name, addr, sex, %s, %s, %s from person_info where phone_num=%s"
        val = (temp, accuracy, frame, person_num)
    else:
        sql = "INSERT INTO electronic_list (Date, Time, phone_num, person_name, addr, sex, temperature, accuracy, img) values (now(), now(), '-', '-', '-', '-', %s, %s, %s)"
        val = (temp, accuracy, frame)
    cursor.execute(sql, val)
    db.commit()
    db.close()
