#! /usr/bin/env python
import sys
import subprocess
from  multiprocessing import Pool

def worker(host):
  args = ['ssh', host, 'python', 'get_cpu_usage.py']
  p = subprocess.Popen(args, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
  out, err = p.communicate()
  return host, out

def cpu_usage():
  hosts = []
  for i in range(2, 97):
    host = 'galaxy{:03d}'.format(i)
    hosts.append(host)

  pool = Pool(processes=96)
  return pool.map(worker, hosts)

if __name__ == '__main__':
  for u in cpu_usage():
    print(u)



  
