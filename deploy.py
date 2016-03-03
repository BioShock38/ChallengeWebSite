#!/usr/bin/python
import os
import getpass
import socket
import sys

if getpass.getuser()+'@'+socket.gethostname() != "challengewebsite@timc-bcm-15.imag.fr":
    sys.exit("This script must be run as challengewebsite@timc-bcm-15.imag.fr user on the release server.")

# git pull
os.system("git fetch")
os.system("git reset --hard origin/master")

# Toggle DEBUG
from tempfile import mkstemp
from shutil import move
from os import remove, close
def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
replace("challengewebsite/settings.py", "DEBUG = True", "DEBUG = False")

# Migration
os.system("./manage.py makemigrations")
os.system("./manage.py migrate")
os.system("./manage.py collectstatic")
