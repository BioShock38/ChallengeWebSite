#!/usr/bin/python
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("152.77.240.65", username="challengewebsite", password="timcimag" )
stdin, stdout, stderr = client.exec_command('cd ChallengeWebSite; pwd; git pull')
stdin, stdout, stderr = client.exec_command('pwd')
print "stderr: ", stderr.readlines()
print "pwd: ", stdout.readlines()
