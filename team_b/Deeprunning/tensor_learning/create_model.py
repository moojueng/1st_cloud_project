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
from tensorflow.keras.callbacks import ReduceLROnPlateau , EarlyStopping , ModelCheckpoint , LearningRateScheduler
from tensorflow.keras.applications import Xception, ResNet50V2
#from tensorflow.keras.applications.xception import preprocess_input as pre_input
from tensorflow.keras.applications.resnet_v2 import preprocess_input as pre_input
import tensorflow as tf
import matplotlib.pyplot as plt
import collections

IMAGE_DIR = '/home/gugu/Project/Deeprunning/tensor_learning/'

def make_person_dataframe(image_dir = IMAGE_DIR):
    paths = []
    label_gubuns = []
    for dirname, _, filenames in os.walk(image_dir):
        for filename in filenames:
            if '.jpg' in filename:
                file_path = dirname+'/'+filename
                paths.append(file_path)#파일 경로 저장
                start_pos = file_path.find('/', 34)
                end_pos = file_path.rfind('/')
                imsi_breed = file_path[start_pos+1:end_pos]
                breed = imsi_breed[:imsi_breed.find('_')]
                label_gubuns.append(breed)#라벨구분을 넣어주기
    data_df = pd.DataFrame({'path':paths, 'label':label_gubuns})#각 파일에 대한 라벨 프레임 만들기
    print(f"데이터 라벨 갯수: {data_df['label'].value_counts()}")
    return data_df

def get_train_valid(train_df, valid_size=0.3, random_state=2022):
    train_path = train_df['path'].values
    train_label = pd.get_dummies(train_df['label']).values
    li = [0,0,0,0]
    tr_path, val_path, tr_label, val_label = train_test_split(train_path, train_label, test_size=valid_size, random_state=random_state, stratify=train_label)
    for i in tr_label:
        li[np.argmax(i)] += 1
    print(li) #class가 잘 분배 되있는지 확인
    li = [0,0,0,0]
    for i in val_label:
        li[np.argmax(i)] += 1
    print(li)
    print('tr_path shape:', tr_path.shape, 'tr_label shape:', tr_label.shape, 'val_path shape:', val_path.shape, 'val_label shape:', val_label.shape)
    return tr_path, val_path, tr_label, val_label

BATCH_SIZE = 8
IMAGE_SIZE = 224

class Breed_Dataset(Sequence):
    def __init__(self, image_filenames, labels, image_size=IMAGE_SIZE, batch_size=BATCH_SIZE, augmentor=None, shuffle=False, pre_func=None):
        self.image_filenames = image_filenames
        self.labels = labels
        self.image_size = image_size
        self.batch_size = batch_size
        self.augmentor = augmentor
        self.pre_func = pre_func
        self.shuffle = shuffle
        if self.shuffle:
            pass

    def __len__(self):
        return int(np.ceil(len(self.labels) / self.batch_size))

    def __getitem__(self, index):
        image_name_batch = self.image_filenames[index*self.batch_size:(index+1)*self.batch_size]
        if self.labels is not None:
            label_batch = self.labels[index*self.batch_size:(index+1)*self.batch_size]
        image_batch = np.zeros((image_name_batch.shape[0], self.image_size, self.image_size, 3), dtype='float32')
        for image_index in range(image_name_batch.shape[0]):
            image = cv2.imread(image_name_batch[image_index])
            if self.augmentor is not None:
                image = self.augmentor(image=image)['image']
            image = cv2.resize(image, (self.image_size, self.image_size))
            if self.pre_func is not None:
                image = self.pre_func(image)
            image_batch[image_index] = image
        return image_batch, label_batch

def create_model(model_type='xception', in_shape=(224, 224, 3), n_classes=4):
    input_tensor = Input(shape=in_shape)
    if model_type == 'resnet50v2':
        base_model = tf.keras.applications.ResNet50V2(include_top=False, weights='imagenet', input_tensor=input_tensor)
    elif model_type == 'xception':
        base_model = tf.keras.applications.Xception(include_top=False, weights='imagenet', input_tensor=input_tensor)

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.3)(x)
    preds = Dense(units=n_classes, activation='softmax')(x)
    model = Model(inputs=input_tensor, outputs=preds)
    with open("model_layer.txt", "w") as fh:
        model.summary(print_fn=lambda x: fh.write(x + '\n'))
    return model

N_EPOCHS = 200

def train_model(model_type, train_df, initial_lr=0.001, augmentor=None, input_pre_func=None):
    tr_path, val_path, tr_label, val_label = get_train_valid(train_df, valid_size=0.3, random_state=2022)
    print(tr_path[:10], tr_label[:10])
    print(f"학습 데이터 개수: {len(tr_label)}\nval 데이터 개수: {len(val_label)}")
    tr_ds = Breed_Dataset(tr_path, tr_label, image_size=IMAGE_SIZE, batch_size=BATCH_SIZE,
                          augmentor=augmentor, shuffle=True, pre_func=input_pre_func)
    val_ds = Breed_Dataset(val_path, val_label, image_size=IMAGE_SIZE, batch_size=BATCH_SIZE,
                          augmentor=None, shuffle=False, pre_func=input_pre_func)

    print('#######', model_type, ' 생성 및 학습 수행 ########')
    model = create_model(model_type=model_type)
    model.compile(optimizer=Adam(lr=initial_lr), loss='categorical_crossentropy', metrics=['accuracy'])

    sav_cb = ModelCheckpoint(filepath='/home/gugu/Project/Deeprunning/tensor_learning/Model/weights.{epoch:03d}-{val_loss}.hdf5', monitor='val_loss', mode='min', save_best_only=True, save_weights_only=True)
    rlr_cb = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=30, mode='min', verbose=1)
    ely_cb = EarlyStopping(monitor='val_loss', patience=150, mode='min', verbose=1)

    history = model.fit(tr_ds, epochs=N_EPOCHS, steps_per_epoch=int(np.ceil(tr_path.shape[0]/BATCH_SIZE)), validation_data=val_ds, validation_steps=int(np.ceil(val_path.shape[0]/BATCH_SIZE)), callbacks=([sav_cb, rlr_cb, ely_cb]), verbose=1)
    return model, history

data_df = make_person_dataframe(image_dir=IMAGE_DIR)
train_df, test_df = train_test_split(data_df, test_size=0.1, stratify=data_df['label'], random_state=2022)
print(f"학습 데이터(valid전): {len(train_df)}\n테스트 데이터: {len(test_df)}")
#model, history = train_model(model_type='xception', train_df=train_df, initial_lr=0.0001, augmentor=None, input_pre_func=pre_input)
model, history = train_model(model_type='resnet50v2', train_df=train_df, initial_lr=0.0001, augmentor=None, input_pre_func=pre_input)

test_path = test_df['path'].values
test_label = pd.get_dummies(test_df['label']).values

# gt_class 컬럼으로 label값을 OHE에서 가장 큰 위치의 인덱스 값으로 Label encoding
test_df['gt_class'] = np.argmax(test_label, axis=1)
test_ds = Breed_Dataset(test_path, test_label, image_size=IMAGE_SIZE, batch_size=BATCH_SIZE, augmentor=None, shuffle=False, pre_func=pre_input)
print(model.evaluate(test_ds))

predict_result = model.predict(test_ds, steps=int(np.ceil(len(test_label)/BATCH_SIZE)))
predict_class = np.argmax(predict_result, axis=1)
test_df['pred_class'] = predict_class
print(test_df[test_df['gt_class'] != test_df['pred_class']]['label'].value_counts())

fig, loss_ax = plt.subplots()

#acc_ax = loss_ax.twinx()

loss_ax.plot(history.history['loss'], 'y', label='train loss')
loss_ax.plot(history.history['val_loss'], 'r', label='val loss')

#acc_ax.plot(history.history['accuracy'], 'b', label='train acc')
#acc_ax.plot(history.history['val_accuracy'], 'g', label='val acc')

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
#acc_ax.set_ylabel('accuray')

loss_ax.legend(loc='upper right')
#acc_ax.legend(loc='lower left')
plt.show()
