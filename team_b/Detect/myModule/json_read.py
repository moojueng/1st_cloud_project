import json
import os
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense , Conv2D , Dropout , Flatten , Activation, MaxPooling2D , GlobalAveragePooling2D
from tensorflow.keras.applications import Xception, ResNet50V2
import tensorflow as tf

def create_model(model_type, in_shape=(224, 224, 3), n_classes=4):
    input_tensor = Input(shape=in_shape)
    if model_type == 'resnet50v2':
        base_model = tf.keras.applications.ResNet50V2(include_top=False, weights=None, input_tensor=input_tensor)
    elif model_type == 'xception':
        base_model = tf.keras.applications.Xception(include_top=False, weights=None, input_tensor=input_tensor)

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.3)(x)
    preds = Dense(units=n_classes, activation='softmax')(x)
    model = Model(inputs=input_tensor, outputs=preds)
    return model

def Json(file_path):
    with open(file_path, "r") as fp:
        info = json.load(fp)
    #new_model = create_model(model_type="resnet50v2")
    new_model = create_model(model_type="xception")
    new_model.load_weights(info['model_PATH'])
    return info['server_host'], info['server_port'], info['user'], info['passwd'], info['db'], info['charset'], info['person_num'], new_model, info['mjpg_PATH'], info['socket_ip'], info['socket_port'], info['frame_path']
