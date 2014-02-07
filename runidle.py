#! /usr/bin/env python3

from sshtaskmanager import SSHTaskManager

connecttimeout = 5
command = input('input the command you want to run:')

nullfile = open('/dev/null', 'w')
tasks = SSHTaskManager(connecttimeout)

for i in range(1, 97):
  host = 'galaxy{:03d}'.format(i)
  tasks.submit(host, command, stdout=nullfile)

tasks.join()




  
