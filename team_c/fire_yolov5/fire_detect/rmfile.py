import os
import shutil
import time

rmfile_PATH = 'C:/yolov5-master/runs/detect'

if os.path.exists(rmfile_PATH):
    shutil.rmtree(rmfile_PATH)