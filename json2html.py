#!/usr/bin/python -tt

import sys
import json
from geoip import geolite2

def html_header():
  print '<!DOCTYPE html>'
  print '<html>'
  print '<head>'
  print '<style>'
  print 'table {'
  print '  font-family: arial, sans-serif;'
  print '  border-collapse: collapse;'
  print '  width: 100%;'
  print '}'

  print 'td, th {'
  print '  border: 1px solid #dddddd;'
  print '  text-align: left;'
  print '  padding: 8px;'
  print '}'
  print ' tr:nth-child(even) {'
  print '   background-color: #dddddd;'
  print ' }'
  print '</style>'
  print '</head>'
  print '<body>'

def html_footer():
  print '</body>'
  print '</html>'


def main():

  addr = dict()
  data_file = '/tmp/data.json'

  fin = open(data_file, 'r')
  json_data = json.load(fin)
  start_stop = json_data['start_stop']
  addr = json_data['addr']
  fin.close()

  html_header()
  print '<table style="width:75%">'
  print '<caption>Email Access Data</caption>'
  print '<tr>'
  print '<td>Start Time</td><td>Stop Time</td><td></td>'
  print '</tr>'
  print '<tr>'
  for tstamp in start_stop:
    print '<td>%s</td>' % tstamp
  print '<td></td>'
  print '</tr>'
  print '<tr>'
  print '<th>email</th><th>IP address</th><th>Count</th><th>Location</th>'
  print '</tr>'
  for email in addr.keys():
    d = addr[email]
    ips = sorted(d, key=d.get, reverse=True)
    match = geolite2.lookup(ips[0])
    if match is not None:
      tz = match.timezone
    else:
      tz = 'Unknown'
    print '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (email, ips[0], d[ips[0]], tz)
    for ip in ips[1:]:
      match = geolite2.lookup(ip)
      if match is not None:
        tz = match.timezone
      else:
        tz = 'Unknown'
      print '<tr><td></td><td>%s</td><td>%s</td><td>%s</td></tr>' % (ip, d[ip], tz)
  print '</table>'
  html_footer()

#  print json.dumps(addr)

if __name__ == "__main__":
  main()
