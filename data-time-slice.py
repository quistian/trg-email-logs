#!/usr/bin/python -tt

import sys
import datetime
import time

# Pop3 SSL log format
# 2017-04-18 00:39:51.793505500 INFO: LOGIN, user=no-reply1@charityhelp.org, ip=[99.230.45.69]
# Imap4 and IMAP4-SSL format
# 2017-04-17 06:54:31.409298500 INFO: LOGIN, user=steversp2@thinkrenewables.com, ip=[75.98.19.133], protocol=IMAP

def tstamp2datetime(log_line):
  ff = log_line.split(' ')
  iso_date = ff[0]
  iso_time = ff[1]
  dd = iso_date.split('-')
  yr = int(dd[0])
  mth = int(dd[1])
  day = int(dd[2])
  tt = iso_time.split(':')
  hr = int(tt[0])
  min = int(tt[1])
  fs = tt[2]
  ss = fs.split('.')
  sec = int(ss[0])
  tau = datetime.datetime(yr, mth, day, hr, min, sec)
  return tau

def main():

  delta_days = int(sys.argv[1])
  delta_hrs = int(sys.argv[2])
  delta_secs = delta_hrs * 3600
  now = datetime.datetime.now()
  ago = now - datetime.timedelta(delta_days, delta_secs)
  print 'now', now
  print 'ago', ago
  for line in sys.stdin:
    if 'INFO: LOGIN,' in line:
      line = line.strip()
      whence = tstamp2datetime(line)
      if whence > ago:
        print line

if __name__ == "__main__":
  main()
