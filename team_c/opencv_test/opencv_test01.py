import cv2
import os
import glob

count = 0
files = glob.glob("C:/code/python/opencv_test/non_f/*.png")
path_F = "C:/code/python/opencv_test/non_f/"
path_save_F = "C:/code/python/opencv_test/cvt_non_f/"
path_png = ".png"

print("파일 길이 :", len(files))
print(str(path_F) + str(count) + str(path_png))

while count < len(files):
    img = cv2.imread(str(path_F) + str(count) + str(path_png), cv2.IMREAD_COLOR)
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2XYZ)
    cv2.imwrite(str(path_save_F) + str(count) + str(path_png), img2)
    cv2.imshow("image", img2)
    count += 1
    cv2.waitKey(0)