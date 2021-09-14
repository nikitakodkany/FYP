
import os
os.chdir("/home/gpkulam/Documents/GCD/gpkulam")
i = 1
for file in os.listdir():
    src=file
    dst = str(i).zfill(5)+".csv"
    os.rename(src,dst)
    i += 1