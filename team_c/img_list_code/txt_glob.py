import glob

input_dir='C:/code/yolov5/fire/images/'
f = open('./train_list.txt', 'w')
input_file=glob.glob(input_dir+'*.jpg')

for file in input_file:
    f.write(file[:41]+'\n')
f.close()


f = open('./val_list.txt', 'w')

for file in input_file:
    f.write(file[:41]+'\n')
f.close()