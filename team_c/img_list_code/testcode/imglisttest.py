#%% 1 ===========================================================
from glob import glob
import os

for f in glob(os.path.join('C:/Users/5/Desktop/dog/*.jpg')):
    print(f)

#%% 2 ===========================================================
import glob

# 대상 폴더
# image_directory = "C:/Users/jangj/Desktop/label/darkflow/dog"

# # 확장자
# extension = "*.jpg"

# 텍스트 파일이 저장될 경로
save_at = "C:/Users/5/Desktop/dog/dog.txt"

# 대상 폴더에서 지정한 확장자를 가진 파일들의 경로를 리스트화
files = sorted(glob.glob("C:/Users/5/Desktop/dog/*.jpg"))

# 파일들의 경로를 텍스트 파일에 추가 및 출력
for file in files:
    f = open(save_at, 'w')
    f.write(file + "\n")
    f.close()
    print(file)

#%% 3 ===========================================================
import glob
import os
files = sorted(glob.glob("C:/Users/5/Desktop/dog/*.jpg"))

print(files)

#%% 4 ===========================================================
word_list = ['abc-123', 'def-456', 'ghi-789', 'abc-456']

search = 'abc'
for i, word in enumerate(word_list):
    if search in word: 
        print('>> modify: ' + word)
        word_list[i] = word.strip(search)

print(word_list)

#%% 5 ===========================================================
import glob
import os

files = sorted(glob.glob("C:/Users/5/Desktop/dog/*.jpg"))
search = 'C:/Users/5/Desktop/'
print(search)
for i, word in enumerate(files):
    if search in word: 
        print('>> modify: ' + word)
        files[i] = word.strip(search)

print(files)

#%% 6 ===========================================================
import glob
import os

files = sorted(glob.glob("C:/Users/5/Desktop/dog/*.jpg"))
search = 'C:/Users/5/Desktop/'

for i, refile in enumerate(files):
    if search in refile: 
        files[i] = refile.strip(search)

print(files)

#%% 7 ===========================================================
import glob
import os

save_at = "C:/Users/5/Desktop/dog/dog.txt"

files = sorted(glob.glob("C:/Users/5/Desktop/dog/*.jpg"))
search = "C:/Users/5/"

for i, refile in enumerate(files):
    if search in refile:
        print('>> modify : ' + refile) 
        files[i] = refile.strip(search)
print(files)

# for file in files:
#     f = open(save_at, 'a')
#     f.write(file + "\n")
#     f.close()
#     print(file)

#%% 8 ===========================================================
list1 = ["apple", "orange", "melon", "banana"]
list2 = []

print("치환전：{0}".format(list1))

for item in list1:

    #문자열 치환
    item_mod = item.replace("apple", "orange")

    # 새로운 리스트에 추가
    list2.append(item_mod)

print("치환후：{0}".format(list2))

#%% 9 ===========================================================
import glob
import os

save_at = "C:/Users/5/Desktop/dog/dog.txt"
files = str(sorted(glob.glob("C:/Users/5/Desktop/dog/*.jpg")))
search = "C:/Users/5"
files2 = []

for i, refile in enumerate(files):
    if search in refile: 
        files[i] = refile.strip(search)
#    print(files)

    for j in files:
        fileschg = j.replace("\\", "/")
        files2.append(fileschg)
        print(files2)

# for file in files2:
#     f = open(save_at, 'a')
#     f.write(file + "\n")
#     f.close()
#     print(file)

#%% 10 ===========================================================
import glob
import os
import re

save_at = "C:/Users/5/Desktop/dog/dog.txt"
files = sorted(glob.glob("C:/Users/5/Desktop/dog/*.jpg"))
search = "C:/Users/5"
files2 = []
#print(files)

for i, refile in enumerate(files):
    if search in refile:
        print('변경대상 : ' + refile)
        files[i] = refile.strip(search)
#print(files)

for j in files:
        fileschg = str(j.replace("\\", "/"))
        files2.append(fileschg)
        #print(files2)

for file3 in files2:
    f = open(save_at, 'a')
    f.write(file3 + "\n")
    f.close()
    print(file3)