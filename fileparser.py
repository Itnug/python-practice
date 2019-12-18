import glob
import os
os.chdir("D:/folder")
for file in glob.glob("*.txt"):
    print(file)
