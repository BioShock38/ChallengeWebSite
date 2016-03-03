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

# Migration
os.system("./manage.py makemigrations")
os.system("./manage.py migrate")
os.system("./manage.py collectstatic")
