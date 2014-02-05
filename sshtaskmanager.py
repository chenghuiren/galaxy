import sys
import os
import subprocess
from threading import Thread

class SSHTaskThread(Thread):
  def __init__(self, host, command, connecttimeout, stdin, stdout, stderr):
    Thread.__init__(self)
    self.host = host
    self.connecttimeout = connecttimeout
    self.command = command
    self.stdin = stdin
    self.stdout = stdout
    self.stderr = stderr

  def run(self):
    self.ret = subprocess.call(['ssh', '-o ConnectTimeout={}'.format(self.connecttimeout), self.host, self.command], stdin=self.stdin, stdout = self.stdout, stderr = self.stderr)

    print('host', self.host, 'done:', 'failed(code={})'.format(self.ret) if self.ret != 0 else 'successful')

class SSHTaskManager:
  def __init__(self, connecttimeout):
    self.connecttimeout = connecttimeout
    self.threads = []

  def submit(self, host, command, stdin = None, stdout = None, stderr = None):
    thread = SSHTaskThread(host, command, self.connecttimeout, stdin, stdout, stderr)
    self.threads.append(thread)
    thread.start()

  def join(self):
    for thread in self.threads:
      thread.join()

    print('#'*20, end='')
    print('success list', end='')
    print('#'*20)
    for thread in self.threads:
      if thread.ret == 0:
        print(thread.host, 'successfull')

    print('#'*20, end='')
    print('failing list', end='')
    print('#'*20)
    for thread in self.threads:
      if thread.ret:
        print(thread.host, 'failed, error code:', thread.ret)







