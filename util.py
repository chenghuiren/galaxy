#! /usr/bin/env python
import subprocess

def getCPUUsage(hostname, interval, count):
  cmd = 'mpstat -P ALL {} {}'.format(interval, count)
  print(cmd)

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

def getWho(hostname):
  cmd = 'who'

  p = subprocess.Popen(['ssh', '-t', '-o ConnectTimeout=5', hostname, cmd], stdout = subprocess.PIPE, stderr = subprocess.PIPE)  

  out, err = p.communicate()

  if out == "":
    return None

  lines = out.split('\n')

  users = []

  for line in lines:
    columns = line.split()

    if len(columns) == 0: 
      continue

    users.append(columns[0])

  return users
