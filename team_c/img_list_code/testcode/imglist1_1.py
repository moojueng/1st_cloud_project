import glob
import os

save_at = "C:/Users/5/Desktop/dog/dog.txt"

files = sorted(glob.glob("C:/Users/5/Desktop/dog/*.jpg"))
search = "C:/Users/5/"

for i, refile in enumerate(files):
    if search in refile:
        files[i] = refile.strip(search)

#print(files)

for file in files:
    f = open(save_at, 'a')
    f.write(file + "\n")
    f.close()
    print(file)