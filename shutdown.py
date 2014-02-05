#! /usr/bin/env python3

import sys
from subprocess import call

hostrange = range(96, 0, -1)
connecttimeout = 5

confirm = input('are you sure you want to shutdown all machines?:[y/N]:')
if confirm != 'y' and confirm != 'Y':
  print('shutdown is canceled')
  sys.exit(1)

print('shutting down all machines...')

for i in hostrange:
  host = 'galaxy{:03d}'.format(i)
  command = 'shutdown -h now'

  print('shutting down', host, '...')
  call(['ssh', '-o ConnectTimeout={}'.format(connecttimeout), host, command])
   
