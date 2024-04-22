import sys
import cvlib as cv
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import Sequence
import sklearn
import cv2
import albumentations as A
from tensorflow.keras.models import Sequential , Model
from tensorflow.keras.layers import Input, Dense , Conv2D , Dropout , Flatten , Activation, MaxPooling2D , GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam , RMSprop
from tensorflow.keras.regularizers import l2
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.applications import ResNet50V2
import tensorflow as tf

def create_model(model_type='xception', in_shape=(224, 224, 3), n_classes=4):
    input_tensor = Input(shape=in_shape)
    if model_type == 'resnet50v2':
        base_model = tf.keras.applications.ResNet50V2(include_top=False, weights=None, input_tensor=input_tensor)
    elif model_type == 'xception':
        base_model = tf.keras.applications.Xception(include_top=False, weights=None, input_tensor=input_tensor)
    elif model_type == 'efficientnetb0':
        base_model = tf.keras.applications.EfficientNetB0(include_top=False, weights=None, input_tensor=input_tensor)
    elif model_type == 'efficientnetb1':
        base_model = tf.keras.applications.EfficientNetB1(include_top=False, weights=None, input_tensor=input_tensor)

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.3)(x)
    preds = Dense(units=n_classes, activation='softmax')(x)
    model = Model(inputs=input_tensor, outputs=preds)
    with open("model_layer.txt", "w") as fh:
        model.summary(print_fn=lambda x: fh.write(x + '\n'))

    return model

new_model = create_model(model_type='resnet50v2')
new_model.load_weights('/home/gugu/Project/model/resnet50v2/best.hdf5')

labels = ["최","안", "조", "심"]
capture = cv2.VideoCapture(0)
count = 0
while True:
    retval, frame = capture.read()
    face, confidence = cv.detect_face(frame)
    count += 1
    if confidence and confidence[0] > 0.9:
        for idx, f in enumerate(face):
            face_in_img = frame[f[1]:f[3], f[0]:f[2], :]
            if type(face_in_img) != type(None) and count >= 5:
                resize_frame = cv2.resize(face_in_img, (224, 224), interpolation=cv2.INTER_NEAREST)
                shape_frame = resize_frame.reshape(-1, 224, 224, 3)/255
                r = new_model.predict(shape_frame, batch_size = 1, verbose=1)
                #print(r)
                res = r[0]
                #print(np.max(res)*100)
                print(res, labels[np.argmax(res)])
                count = 0
                cv2.imshow("resize", resize_frame)
    if not retval:
        break
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()

cv2.destroyAllWindows()
