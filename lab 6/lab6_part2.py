#List directories, files, and all content in a path:
import os

path =  "C:\\Users\\Sattigali\\Desktop\\PP2\\lab 6"

if os.path.exists(path):
    print("Directories:")
    print([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])

    print("Files:")
    print([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])

    print("All:")
    print(os.listdir(path))
else:
    print("Path does not exist:", path)
print()



#Check access to a path (existence, read, write, execute):
import os

path =  "C:\\Users\\Sattigali\\Desktop\\PP2\\lab 6"

print("Exists:", os.access(path, os.F_OK))
print("Readable:", os.access(path, os.R_OK))
print("Writable:", os.access(path, os.W_OK))
print("Executable:", os.access(path, os.X_OK))
print()



#Check if path exists and get filename and directory:
import os

path =  "C:\\Users\\Sattigali\\Desktop\\PP2\\lab 6"

if os.path.exists(path):
    print("Directory:", os.path.dirname(path))
    print("Filename:", os.path.basename(path))
else:
    print("Path does not exist.")
print()



#Count number of lines in a text file:

file_path = "C:\\Users\\Sattigali\\Desktop\\PP2\\lab 6\\1.py"

with open(file_path, 'r') as f:
    lines = f.readlines()
    print("Line count:", len(lines))
print()


#Write a Python program to write a list to a file.
my_list = ['besh', 'baursak', 'tea']
with open("eda.txt", 'w') as f:
    for item in my_list:
        f.write(f"{item}\n")

print()




#Write a Python program to generate 26 text files named A.txt, B.txt, and so on up to Z.txt
import string

for letter in string.ascii_uppercase:
    with open(f"{letter}.txt", 'w') as f:
        f.write(f"This is file {letter}.txt\n")
print()



#Write a Python program to copy the contents of a file to another file

import shutil

source = "copy.txt"
destination = "copy2.txt"

shutil.copyfile(source, destination)
print()

#Write a Python program to delete file by specified path. Before deleting check for access and whether a given path exists or not.

import os

path = "file_delete.txt"

if os.path.exists(path):
    if os.access(path, os.W_OK):
        os.remove(path)
        print("File deleted")
    else:
        print("No access")
else:
    print("File does not exist")
