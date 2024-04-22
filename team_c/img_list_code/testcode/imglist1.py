import glob

# 대상 폴더
# image_directory = "C:/Users/jangj/Desktop/dog"

# # 확장자
# extension = "*.jpg"

# 텍스트 파일이 저장될 경로
save_at = "C:/Users/5/Desktop/dog/dog.txt"

# 대상 폴더에서 지정한 확장자를 가진 파일들의 경로를 리스트화
files = sorted(glob.glob("C:/Users/5/Desktop/dog/*.jpg"))

# 파일들의 경로를 텍스트 파일에 추가 및 출력
for file in files:
    f = open(save_at, 'a')
    f.write(file + "\n")
    f.close()
    print(file)