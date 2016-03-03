#!/usr/bin/python
import os

# git pull
os.system("git pull")


# Migration
os.system("./manage.py makemigrations")
os.system("./manage.py migrate")
os.system("./manage.py collectstatic")
