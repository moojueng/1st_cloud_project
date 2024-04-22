import numpy as np # linear algebra
import os
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense , Conv2D , Dropout , Flatten , Activation, MaxPooling2D , GlobalAveragePooling2D
from tensorflow.keras.applications import Xception
import tensorflow as tf

def create_model(model_type='xception', in_shape=(224, 224, 3), n_classes=4):
    input_tensor = Input(shape=in_shape)
    base_model = tf.keras.applications.Xception(include_top=False, weights='imagenet', input_tensor=input_tensor)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.3)(x)
    preds = Dense(units=n_classes, activation='softmax')(x)
    model = Model(inputs=input_tensor, outputs=preds)
    return model

new_model = create_model()
new_model.load_weights('/home/gugu/Project/back/tensor_learning/Model/all/weights.464-4.431459274201188e-06.hdf5')
