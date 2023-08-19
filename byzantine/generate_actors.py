
# Python program to create the duplicate of
# an already existing file
import shutil
import os

# src contains the path of the source file
src_alice = r"app_alice.py"
src_bob = r"app_bob.py"

n = 5

for i in range(n):

    # dest contains the path of the destination file
    dest_alice = r"app_alice" + str(i) + ".py"
    dest_bob = r"app_bob" + str(i) + ".py"
    
    # create duplicate of the file at the destination,
    # with the name mentioned
    # at the end of the destination path
    # if a file with the same name doesn't already
    # exist at the destination,
    # a new file with the name mentioned is created
    path_alice = shutil.copyfile(src_alice , dest_alice)
    path_bob = shutil.copyfile(src_bob , dest_bob)
