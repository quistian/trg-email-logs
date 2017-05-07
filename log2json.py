#!/usr/bin/python -tt

import sys
import json
import re

def add2dict(d, email, ip):
  if email in d:
    if ip in d[email]:
      d[email][ip] += 1
    else:
      d[email][ip] = 1
  else:
    d[email] = {ip : 1}

def main():
  
  addr = dict()
  data_file = '/tmp/data.json'
  start_stop = ['start', 'stop']

# Pop3 SSL log format
# 2017-04-18 00:39:51.793505500 INFO: LOGIN, user=no-reply1@charityhelp.org, ip=[99.230.45.69]
# Imap4 and IMAP4-SSL format
# 2017-04-17 06:54:31.409298500 INFO: LOGIN, user=steversp2@thinkrenewables.com, ip=[75.98.19.133], protocol=IMAP

# read input into an array
  lines = []
  for line in sys.stdin:
    if 'INFO: LOGIN' in line:
      line = line.strip()
      lines.append(line)
  for line in lines:
      fields = line.split(',')
      email = fields[1].split('=')[1]
      ip = fields[2].split('=')[1][1:-1]
      add2dict(addr, email, ip)

  ff = lines[0].split()
  start_stop[0] = ' '.join(ff[:2]) 
  ff = lines[-1].split()
  start_stop[1] = ' '.join(ff[:2])

  json_data = {
    'addr': addr,
    'start_stop': start_stop
  }

  fout = open(data_file, 'w')
  json.dump(json_data, fout)
  fout.close()
  
#  print json.dumps(json_data)

if __name__ == "__main__":
  main()
