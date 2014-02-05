#! /usr/bin/env python3

from sshtaskmanager import SSHTaskManager

connecttimeout = 5
software = input('input the software name you want to install:')
print('installing software:', software)

nullfile = open('/dev/null', 'w')
tasks = SSHTaskManager(connecttimeout)

for i in range(1, 97):
  host = 'galaxy{:03d}'.format(i)
  command = 'apt-get install -y ' + software
  tasks.submit(host, command, stdout=nullfile)

tasks.join()




  
