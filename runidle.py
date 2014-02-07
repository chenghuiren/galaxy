#! /usr/bin/env python3
import util
import asyncproc
import os
import multiprocessing

def worker(hostname, cmd):
  started = False
  p = None
  while True:
    users = util.getWho(hostname)
    otherUser = False
    for user in users:
      if user != 'chren' and user != 'root':
        otherUser = True
        break

    if started and not otherUser:
      poll = p.wait(os.WNOHANG)

      out = p.read()
      if out != '': 
        print(hostname + ':' + out)

      if poll != None: 
        print(hostname + ': finished')
        break

    if started and otherUser:
      print('other users loged in. killing the process...')
      p.terminate()
      print('killed')
      started = False

    if not started and not otherUser:
      print('starting the process...')
      p = asyncproc.Process(['ssh', '-t', hostname, cmd], stdout = subprocess.PIPE, stderr = subprocess.PIPE)  


cmd = input('input command:')

ps = []
for i in range(2, 97):
  hostname = 'galaxy{:03d}'.format(i)

  p = multiprocessing.Process(target = worker, args = (hostname, cmd))
  ps.append(p)
  p.start()
