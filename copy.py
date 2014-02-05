#! /usr/bin/env python3
import sys
import subprocess
from  multiprocessing import Process

argv = sys.argv

src = argv[1]
dst = argv[2]

def worker(host, args):
  subprocess.call(args)
  print(host + ' done')

for i in range(2, 97):
  host = 'galaxy{:03d}'.format(i)
  scpArgs = ['scp', '-r', src, '{}:{}'.format(host, dst)]
  p = Process(target = worker, args=(host, scpArgs))
  p.start()



  
