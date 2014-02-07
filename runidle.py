#! /usr/bin/env python
import util
import asyncproc
import os
import threading
import time
from multiprocessing import Lock

lock = Lock()

def lprint(*args):
  lock.acquire()
  print(' '.join(args))
  lock.release()

def worker(hostname, cmd):
  lprint('hostname, cmd:' + hostname + ',' + cmd)
  started = False
  p = None
  while True:
    users = util.getWho(hostname)
    if users is None:
      lprint('hostname', 'unreachable')
      break

    otherUser = False
    for user in users:
      if user != 'chren' and user != 'root':
        otherUser = True
        break

    if started and not otherUser:
      poll = p.wait(os.WNOHANG)
      out = p.read()
      if out != '': 
        lprint(hostname + ':' + out)
      if poll != None: 
        lprint(hostname + ': finished')
        break
    elif started and otherUser:
      lprint('other users loged in. killing the process...')
      p.terminate()
      lprint('killed')
      started = False
    elif not started and not otherUser:
      lprint('starting the process...')
      p = asyncproc.Process(['ssh', '-t', hostname, cmd])  
      started = True

    time.sleep(5)


cmd = raw_input('input command:')

ps = []
for i in range(2, 10):
  hostname = 'galaxy{:03d}'.format(i)

  p = threading.Thread(target = worker, args = (hostname, cmd))
  ps.append(p)
  p.start()
