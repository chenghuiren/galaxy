#! /usr/bin/env python3

from sshtaskmanager import SSHTaskManager
from subprocess import call

connecttimeout = 5
hostrange = range(1,97)
username = input('input username:')
password = input('input password:')

prefix = '.pw'

tasks = SSHTaskManager(connecttimeout)

nullfile = open('/dev/null', 'w')

pwfilenames = []
pwfiles = []
for i in hostrange:
  host = 'galaxy{:03d}'.format(i)
  command = 'passwd ' + username

  pwfilename = prefix + '.' + host
  pwfilenames.append(pwfilename)

  pwfile = open(pwfilename, 'w')
  print(password, file=pwfile)
  print(password, file=pwfile)
  print('\n'*100, file=pwfile)
  pwfile.close()

  pwfile = open(pwfilename, 'r')
  pwfiles.append(pwfile)
  tasks.submit(host, command, stdin = pwfile, stdout=nullfile)

tasks.join()

for pwfile in pwfiles:
  pwfile.close()

for pwfilename in pwfilenames:
  call(['rm', pwfilename])

