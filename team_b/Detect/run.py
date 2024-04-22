import integ
from myModule import json_read
import time

json_infor = json_read.Json("myModule/info.json")
pro_control = integ.Run(json_infor)
switch = True
while True:
    try:
        state = pro_control.start_stop()
        #사람 검출이 안되면 state = False, 사람 검출이 되면 True
        
        if (state == False and switch) or (state and switch == False):    pass

        elif state and switch:#사람이 검출이 되고 switch가 True이면
            print("검출시작!")
            switch, temper_time = pro_control.detecting()#매커니즘 돌리고 switch가 False가 됨, 온도 측정에 걸린 시간
            detect_time = time.time()#작업이 끝난 시간

        else:
            #사람 검출이 안되고 switch는 내려가있으면
            rate_time = time.time()
            print("지난 시간 확인")
            if rate_time - detect_time - temper_time > 3: switch = True

    except KeyboardInterrupt as a:
        print("프로그램을 종료합니다")
        break

    except Exception as e:
        print(f"예외 발생 {str(e)}")
        continue

del pro_control
