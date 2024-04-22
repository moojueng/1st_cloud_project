import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

img = cv2.imread('/home/gugu/Desktop/2022-04-04-124513.jpg')
img_cvt = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_res = cv2.resize(img_cvt, (224,224), interpolation=cv2.INTER_LANCZOS4)
img_arr = img_res.reshape(-1, 224, 224, 3)/255

model = load_model('/home/gugu/Project/tensor_learning/Model/best.h5')
labels = ["최규범", "안형수", "조하나", "심은용"]

r = model.predict(img_arr, batch_size=64, verbose=1)

res = r[0]

for i, acc in enumerate(res):
    print(labels[i], "=", int(acc*100))
print("---")
print("예측한 결과 = ", labels[res.argmax()])
