import threading
from flask import Flask, Response, render_template
from detect_and_db02 import detect, fire_num
import pymysql

app2 = Flask(__name__)

@app2.route("/")
def index():
    status = None
    db = pymysql.connect(host='20.194.30.39',
                         user='fire',
                         password='0000',
                         charset='utf8',
                         db='fire_detect')
    cursor = db.cursor()
    sql = "SELECT * FROM temper ORDER BY time DESC limit 1;"
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    for record in result:
        if record == None:
            status = "오류"
        else:
            status = "정상"
        return render_template("index2.html", T=record[1], H=record[2], S=status)


@app2.route("/video_feed")
def video_feed():
    return Response(detect(),
        mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__== "__main__":
    thread1 = threading.Thread(target=fire_num)
    thread1.start()
    app2.run(host="0.0.0.0", port="50050")