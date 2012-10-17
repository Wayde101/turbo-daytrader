#!/usr/bin/env python
#$Id: shenzhou.py chao.ou$
'''
    auther:     chao.ou
    description: shenzhou is a class of registing to dataplatform
'''
import string
import simplejson as json
from toolUtil import *
import md5
import time
import getopt
import ConfigParser
import random
import os 
import subprocess

class ShenZhou:
    
    def __init__(self, srcdir, destdir):
        rand = random.randint(0,999)
        cfgParser = ConfigParser.ConfigParser()
        cfgParser.read('yishan2.conf')
        self.host = '172.18.120.21:8080'
#        self.host = '10.32.4.102:8080' 
        self.log_src = ''
        self.log_dest = ''
        self.log_id = ''
        self.email = cfgParser.get('shenzhou', 'email')
        self.dataset = cfgParser.get('shenzhou', 'dataset')
        self.registerdata = ''
        self.process = 0
        self.byte = 0
        self.shenzhoulogID = '843c552c183a4bf9195405f4ce0170fa'
        self.shenzhouregID = 'da93eb196232f66f18d881e42a31e4ef'
        self.type = cfgParser.get('mode', 'fstype')
        self.namenode = cfgParser.get('environment', 'namenode') 
        self.srcnuwa = cfgParser.get('environment', 'srcnuwa')
        self.destnuwa = cfgParser.get('environment', 'destnuwa')
        self.nuwa_port = cfgParser.get('environment', 'nuwa_port')
        
        self.buildList(srcdir, destdir)
        self.regdata = self.makeRegData(srcdir, destdir)
    
    def registerFile(self):
        t = int(time.time())
        s = self.createSign(self.regdata, t, self.shenzhouregID)
        data = {'c':self.regdata, 's':s, 't':t}
        url = "/api_yugong.php" 
        res = doPost(data, self.host, url) 
        if res != False:
            dic_result = json.JSONDecoder().decode(res)
            print dic_result['m'] 
        else:
            print "can not connect to server register Failed" 
        
    def registerDB(self, c, sid):
        pass

#update yugong_log status
    def logYuGong(self, data):
        t = int(time.time())
        s = self.createSign(data, t, self.shenzhoulogID)
        data = {'c':data, 's':s, 't':t}
        url = "/api_yugong_log.php"
        res = doPost(data, self.host, url)
        if res != False:
            dic_result = json.JSONDecoder().decode(res)
            if dic_result['r'] == False:
                print dic_result['m']
                return False
            else:
                return dic_result['d']
        else:
            return False           
    
    def createSign(self, c, time, id):
        str1 = md5.new(c+str(time)).hexdigest()
        str2 = md5.new(id+str(str1)).hexdigest()
        str3 = md5.new(str(time)).hexdigest()
        s = str(str2)+str(str3)
        return s

#build register data to json
    def makeRegData(self, srcdir, destdir):
        dic_data = {"JobUserEmail":self.email, "DataSetName":self.dataset}
        dic_data['FileData'] = []
        filelist = []
        if destdir == '':
            for path in file(srcdir).readlines():
                path = path.strip()
                val = {"Path":path}
                if re.search('\/$', path):
                    val['Type'] = '1'
                else:
                    val['Type'] = '2'
                filelist.append(val)
        else:
            val = {"Path":destdir}
            if re.search('\/$', path):
                val['Type'] = '1'
            else:
                val['Type'] = '2'
            filelist.append(val)
        dic_data['FileData'] = filelist
        strJsonData = json.dumps(dic_data)
        return strJsonData

#set the status in yugong_log
#status: 1---process is sucessful
#        2---process is running
#        3---process is failed
    def makeLogData(self, log_status,log_process='o'):
        if log_process == 'o':
            process = self.process
        else:
            process = log_process
        dic_data = {"JobUserEmail":self.email, "DataSetName":self.dataset, "JobId":self.log_id,"LogMsg":"","LogStatus":log_status,"LogIncreasesize":self.byte,"DataSource":self.log_src,"DataDestination":self.log_dest,"LogProgress":process}
        strJsonData = json.dumps(dic_data)
        self.process = process
        return strJsonData
       
#bulid register file data        
    def buildList(self, srcdir, destdir):
        if destdir == '':
            for path in file(srcdir).readlines():
                path = path.strip()
                if self.type == 'hdfs2pangu':
                    self.log_src += 'hdfs://'+self.namenode+':9000'+path+';'
                    self.log_dest += 'pangu://'+self.destnuwa+":"+self.nuwa_port+path+';'
                elif self.type == 'pangu2pangu':
                    self.log_src += 'pangu://'+self.srcnuwa+':'+self.nuwa_port+path+';'
                    self.log_dest += 'pangu://'+self.destnuwa+":"+self.nuwa_port+path+';'
                else:
                    pass
        else:
            if self.type == 'hdfs2pangu':
                self.log_src += 'hdfs://'+self.namenode+':9000'+srcdir
                self.log_dest += 'pangu://'+self.destnuwa+":"+self.nuwa_port+destdir
            elif self.type == 'pangu2pangu':
                self.log_src += 'pangu://'+self.srcnuwa+':'+self.nuwa_port+srcdir
                self.log_dest += 'pangu://'+self.destnuwa+":"+self.nuwa_port+destdir
            else:
                pass

    def deleteFile(self, filedir):
        if filedir == '':
            print 'no filelist'
            sys.exit(1)
        filehandler = open(filedir, "r")
        dirlist = filehandler.readlines()
        dic_data = {"JobUserEmail":self.email, "DataSetName":self.dataset}
        dic_data['FileData'] = []
        filelist = [] 
        for x in dirlist:
            x = x.strip()
            val = {"Path":x}
            if re.search('\/$', x):
                val['Type'] = '1'
            else:
                val['Type'] = '2'
            filelist.append(val)
        dic_data['FileData'] = filelist
        strJsonData = json.dumps(dic_data)
        t = int(time.time())
        s = self.createSign(strJsonData, t, self.shenzhouregID)
        data = {'c':strJsonData, 's':s, 't':t, 'd':'d'}
        url = "/api_yugong.php" 
        res = doPost(data, self.host, url)
        if res != False:
            dic_result = json.JSONDecoder().decode(res)
            print dic_result['m'] 
        else:
            print "can not connect to server register Failed"








  
