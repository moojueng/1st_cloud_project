import os
import glob
import time

rmfile_PATH = 'C:/yolov5-master/runs/detect'
dir_PATH = 'C:/yolov5-master/runs'
labels_PATH = 'C:/yolov5-master/runs/detect/exp/labels'
txt_PATH = 'C:/yolov5-master/runs/detect/exp/labels/*.txt'

while(True):
    dir_list = os.listdir(labels_PATH)
    dir_count = len(dir_list)
    print(dir_count)
    label_list = sorted(glob.glob(txt_PATH), key=os.path.getctime, reverse=False)
    first_list = label_list[0]
    print(first_list)

    if dir_count > 50:
        os.remove(first_list)
    else:
        pass

    time.sleep(2)