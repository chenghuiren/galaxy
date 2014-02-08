#! /usr/bin/env python
import util
import os
import time
from threading import Lock, Thread
from subprocess import Popen

mtx = Lock()

def isRunning(pid):
  return os.system('ps -p {} &> /dev/null'.format(pid)) == 0

def kill(pid):
  os.system('kill {}'.format(pid))

def lprint(*args):
  mtx.acquire()
  print(' '.join(args))
  mtx.release()

def worker(hostname, cmd):
  lprint('hostname, cmd:' + hostname + ',' + cmd)
  started = False
  pid = None
  while True:
    users = util.getWho(hostname)
    if users is None:
      lprint('hostname', 'unreachable')
      break
    print(users)

    otherUser = False
    for user in users:
      if user != 'chren' and user != 'root':
        otherUser = True
        break

    if started and not otherUser:
      if not isRunning(pid):
        lprint('done')
        break
    elif started and otherUser:
      lprint('other users loged in. killing the process...')
      kill(pid)
      lprint('killed')
      started = False
    elif not started and not otherUser:
      lprint('starting the process...')
      pid = os.fock()
      if pid == 0: 
        Popen(['ssh', '-t', hostname, cmd])
        sys.exit(0)
      else:
        started = True

    time.sleep(1)


cmd = raw_input('input command:')

ps = []
for i in range(2,5):
  hostname = 'galaxy{:03d}'.format(i)

  p = Thread(target = worker, args = (hostname, cmd))
  ps.append(p)
  p.start()

raw_input('press enter to terminate...')
for p in ps:
  p.terminate()
