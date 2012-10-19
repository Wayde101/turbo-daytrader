#!/usr/bin/env python
'''
    auther:     chao.ou
    description: tool for shenzhou
'''
import httplib, urllib
import smtplib
import re
from datetime import date
from time import localtime, strftime 

def send_mail(mail_file, mail_host='smtp.ops.aliyun-inc.com'):
    file = open(mail_file)
    line = file.readline()
    from_addr = line[line.find(':') + 1 :].strip()
    line = file.readline()
    to_addr = line[line.find(':') + 1 :].split(',')
    server = smtplib.SMTP(mail_host)

    file.seek(0)
    body = file.read()
    body = re.sub('^', 'Date:' + strftime("%a, %d %b%Y %H:%M:%S +0800", localtime()) + '\n', body)
    server.sendmail(from_addr, to_addr, body)
    server.quit()

def doPost(data, host, url):
    params = urllib.urlencode(data)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host)
    conn.request("POST", url, params, headers)
    response = conn.getresponse()
    if response.status == 200:
        data = response.read()
        conn.close()
        return data
    else:
        print response.status, response.reason
        return False


def alertWarning(level, info):
    logfile = open('/tmp/shenzhou.log', 'w')
    if level == 'warning':
        content = 'Warning---%s'%(info)
    elif level == 'critical':
        content = 'Critical---%s'%(info)
    elif level == 'error':
        content = 'Error---%s'%(info)
    else:
        content = 'Ok---%s'%(info)
    logfile.write(content)
    logfile.close()

def writeLog(filename, content):
    logfile = open(filename, 'a')
    logfile.write(content)
    logfile.close()
