import glob
import os
import re

#추출된 텍스트를 저장할 경로(정확하게)
save_at = "C:/code/python/opencv_test/fire.txt" 
#추출대상이 되는 폴더 경로 --> dog 폴더안에 .jpg 확장자 모두
files = sorted(glob.glob("C:/code/yolov5/fire/images/*.jpg"))
#추출된 경로에서 제거하고 싶은 경로
search = ""
files2 = []
#print(files)

for i, refile in enumerate(files):
    if search in refile:
        print('변경대상 : ' + refile)
        files[i] = refile.lstrip(search)
        print('제거대상 : ' + search)
#print(files)

for j in files:
        fileschg = str(j.replace("\\", "/"))
        files2.append(fileschg)
        #print(files2)

for file3 in files2:
    f = open(save_at, 'a')
    f.write(file3 + "\n")
    f.close()
    print('추출텍스트 --> ' + file3)