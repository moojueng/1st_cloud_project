import cv2
import sys
import cvlib as cv
 
# loop through frames
def capture(webcam):  
    state = 2#0: non_mask, 1: white, 2: black
    captured_num = state
    person = 3 #0: 규범, 1: 형수, 2: 하나, 3: 은용, 4: 다른사람
    while webcam.isOpened():
        li = ['./01039978450_Choi/01039978450_'+str(captured_num)+'.jpg', 
            './01080082021_An/01080082021_'+str(captured_num)+'.jpg',
            './01085988951_Jo/01085988951_'+str(captured_num)+'.jpg',
            './01097805386_Sim/01097805386_'+str(captured_num)+'.jpg'] 
        # read frame from webcam 
        status, frame = webcam.read()
        if not status:
            break
        # 이미지 내 얼굴 검출
        face, confidence = cv.detect_face(frame)
        print(confidence) 
        if confidence:
            if confidence[0] > 0.9:
                for idx, f in enumerate(face):
                    (startX, startY) = f[0], f[1]
                    (endX, endY) = f[2], f[3]
                    face_in_img = frame[startY:endY, startX:endX, :]
                    cv2.imwrite(li[person], face_in_img) 
                    captured_num = captured_num + 3
                    print('================================')
                    print(captured_num)
        if cv2.waitKey(33) == 27: exit()
        if captured_num >= 900: exit()    
        cv2.imshow("captured frames", frame)        

def main():
    try:
        webcam = cv2.VideoCapture("http://192.168.0.16:9090/?action=stream")
        if not webcam.isOpened():
            print("Could not open webcam")
        while True:
            capture(webcam)
            webcam.release()
            cv2.destroyAllWindows() 
    except cv2.error:
        webcam.release()
        main()

if __name__ == "__main__":  main()
