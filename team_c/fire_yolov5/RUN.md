python train.py --batch 64 --epochs 100 --data ./data/fire.yaml --cfg ./models/yolov5m.yaml --weights yolov5m.pt --name firede

!python train.py --img 416 --batch 32 --epochs 200 --data /content/dataset/data.yaml --cfg ./models/yolov5s.yaml --weights yolov5s.pt --name fire_yolo

(image)
python detect.py --source fire1.jpg --weights best.pt --conf 0.6 --save-txt --nosave

(video)
python detect.py --source fire1.mp4 --weights best.pt --conf 0.6 --save-txt --nosave

(webcam)
python detect.py --source 0 --weights best.pt --conf 0.6 --save-txt --nosave

(RTSP실행)
sudo ./h264_v4l2_rtspserver/v4l2rtspserver -F 25 -W 640 -H 480 -P 5008 /dev/video0

(mjpg실행)
mjpg_streamer -i "input_raspicam.so -x 640 -y 480 -fps 30 -rot 180 -ex night" --output "output_http.so -w /usr/local/share/mjpg-streamer/www --port 50036"

(mjpg YOLO실행)
python detect.py --source "http://192.168.0.11:50036/?action=stream" --weights best.pt --conf 0.5 --save-txt --nosave

(RTSP YOLO실행)
python detect.py --source "rtsp://192.168.0.11:50036/unicast" --weights best.pt --conf 0.5 --save-txt --nosave

(webcam)
python detect.py --source 0 --weights best.pt --conf 0.6 --save-txt --nosave

(cv2 PATH)
import sys
sys.path.append('C:/Users/iOT/AppData/Local/Programs/Python/Python310/Lib/site-packages')
sys.path.append('/home/jangjh45/anaconda3/envs/yolo/lib/python3.7/site-packages')
