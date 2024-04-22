import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os

IMAGE_DIR = '/home/gugu/Project/tensor_learning/IMAGE'

def make_person_dataframe(image_dir = IMAGE_DIR):
    paths = []
    label_gubuns = []
    for dirname, _, filenames in os.walk(image_dir):
        for filename in filenames:
            if '.jpg' in filename:
                file_path = dirname+'/'+filename
                paths.append(file_path)#파일 경로 저장
                start_pos = file_path.find('/', 35)
                end_pos = file_path.rfind('/')
                imsi_breed = file_path[start_pos+1:end_pos]
                breed = imsi_breed[:imsi_breed.find('_')]
                label_gubuns.append(breed)#라벨구분을 넣어주기
    data_df = pd.DataFrame({'path':paths, 'label':label_gubuns})#각 파일에 대한 라벨 프레임 만들기
    return data_df

data_df = make_person_dataframe(IMAGE_DIR)
print(data_df['label'].value_counts())
