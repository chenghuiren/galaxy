#! /usr/bin/env python
import subprocess

def getCPUUsage(hostname, interval, count):
  cmd = 'mpstat -P ALL {} {}'.format(interval, count)
  print(cmd)

  #p = subprocess.Popen(['mpstat', '-P', 'ALL', str(interval), str(count)], stdout = subprocess.PIPE, stderr = subprocess.PIPE)  
  p = subprocess.Popen(['ssh', hostname, cmd], stdout = subprocess.PIPE, stderr = subprocess.PIPE)  
  out, err = p.communicate()
  if err is not None and err != '':
    print(err)
    return None

  lines = out.split('\n')

  averageCount = 0
  usage = []
  for line in lines:
    columns = line.split()

    if len(columns) == 0: 
      continue

    if columns[0] == 'Average:':
      averageCount += 1
      if averageCount > 1:
        usage.append(float(columns[2]))

  return usage

print(getCPUUsage('localhost', 2, 1))
