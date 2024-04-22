import pymysql
 
class Database():
    def __init__(self):
        self.db= pymysql.connect(host='20.194.30.39',
                                 user='fire',
                                 password='0000',
                                 charset='utf8',
                                 db='fire_detect')
        self.cursor= self.db.cursor()
 
    def execute(self, query, args={}):
        self.cursor.execute(query, args)
        row= self.cursor.fetchall()
        return row