#!/usr/bin/env python
# $Id: yishan2.py 26091 2010-04-12 06:51:48Z leo.zhouw $
''' 
    auther :     LiuJinglong
    edit by:     chao.ou
    description: yishan is a wrapper of yugong
'''

import os
import ConfigParser
import string
import getopt
import sys
import time
import subprocess
import random
import StringIO
import re
import simplejson as json
import threading 
from shenzhou import ShenZhou
from toolUtil import *

PM_RUN = '/apsara/deploy/pm_run'
PU = '/apsara/deploy/pu'
RPC_CALLER = '/apsara/deploy/rpc_caller'
ARCH = 'debug'
VERSION = '64'
PACKAGEPATH = '/apsara/deploy/package/'

class YishanConfig:
    def __init__(self,clusterConfPath=None):

        if clusterConfPath == None:
            path = os.path.dirname(__file__)
        else:
            path = clusterConfPath

        configFile = os.path.join(path, 'yishan2.conf')
        print 'YishanConfigFile:',configFile
        assert os.path.exists(configFile)
        self.loadConfig(configFile)

    def loadConfig(self, configPath):
        rand = random.randint(0,999)
        cfgParser = ConfigParser.ConfigParser()
        cfgParser.read(configPath)
        self.apsara_home = cfgParser.get('environment', 'apsara_home')
        self.yu2_home = cfgParser.get('environment', 'yu2_home')
        self.srcnuwa = cfgParser.get('environment', 'srcnuwa')
        self.destnuwa = cfgParser.get('environment', 'destnuwa')
        self.nuwa_port = cfgParser.get('environment', 'nuwa_port')
        self.jre_home = cfgParser.get('environment', 'java_home')
        self.namenode = cfgParser.get('environment', 'namenode')

        self.job_user = cfgParser.get('yugong', 'job_user')
        self.job_name = cfgParser.get('yugong', 'job_name') + str(rand)

        self.hadoop_user = cfgParser.get('yugong', 'hadoop_user')
        self.hadoop_group = cfgParser.get('yugong', 'hadoop_group')

        self.buffer_size = cfgParser.get('yugong', 'buffer_size')
        self.instance_num = cfgParser.get('yugong', 'instance_num')
        self.stonehenge_path = cfgParser.get('yugong', 'stonehenge_path')
        self.type = cfgParser.get('mode', 'fstype') #       hdfs2pangu / pangu2pangu
        self.pangu_mode = cfgParser.get('mode', 'pangu_mode')  # 16 means compress
        self.nuwa_mode = cfgParser.get('mode', 'nuwa_mode')  # src / dest :means yishan2 run in src cluster or dest cluster
                                                             #deprecated this parameter,auto detect it by dayu client

        self.srccap = cfgParser.get('yugong', 'src_pangu_cap')
        self.destcap = cfgParser.get('yugong', 'dest_pangu_cap')
        self.production = GetProduction()
        self.keeptempfile = cfgParser.get('mode', 'keeptempfile')
        
        self.setenv()
    
    def setenv(self):
        #pdb.set_trace()
        os.environ['CLASSPATH'] = '%s:%s/bin/jar/commons-logging-api-1.0.4.jar:%s/bin/jar/hadoop-0.19.1-core.jar:%s/lib/dt.jar:%s/lib/tools.jar:%s/bin/jar/hadoop-0.19.1-core.jar' %(self.jre_home, self.apsara_home, self.apsara_home, self.jre_home, self.jre_home, self.apsara_home)
        #os.environ['CLASSPATH'] = '%s:%s/bin/jar/commons-logging-api-1.0.4.jar:%s/bin/jar/hadoop-0.20.2-core.jar:%s/lib/dt.jar:%s/lib/tools.jar:%s/bin/jar/hadoop-0.20.2-core.jar' %(self.jre_home, self.apsara_home, self.apsara_home, self.jre_home, self.jre_home, self.apsara_home)
        os.environ['LD_LIBRARY_PATH'] = '%s/jre/lib/amd64/server/:%s/bin/lib64/' % (self.jre_home, self.apsara_home) 

    def buildOneStongehenge(self, srcdir, destdir):
        #list = filelist.split(',')
        jsonstring = ''
#for i in range(len(list)):
        jsonstring += "{\n"
        if self.type == 'hdfs2pangu':
            jsonstring += "\t\"sourceType\":\"HDFS\",\n"
            jsonstring += "\t\"sourceDetail\":\n"
            jsonstring += "\t\"{\n"
            jsonstring += "\t\t\\\"Path\\\":\\\"%s\\\",\n" % srcdir
            jsonstring += "\t\t\\\"Host\\\":\\\"%s\\\",\n" % self.namenode
            jsonstring += "\t\t\\\"User\\\":\\\"%s\\\",\n" % self.hadoop_user
            jsonstring += "\t\t\\\"Groups\\\":[\\\"%s\\\"]\n" % (self.hadoop_group)
            jsonstring += "\t}\",\n"
        elif self.type == 'pangu2pangu':
            jsonstring += "\t\"sourceType\":\"PANGU\",\n"
            jsonstring += "\t\"sourceDetail\":\n"
            jsonstring += "\t\"{\n"
            jsonstring += "\t\t\\\"Path\\\":\\\"pangu://%s:%s%s\\\",\n" % (self.srcnuwa, self.nuwa_port, srcdir)
            jsonstring += "\t\t\\\"Capability\\\":\\\"%s\\\"\n" % (self.srccap)
            jsonstring += "\t}\",\n"
        else:
            return -1

        jsonstring += "\t\"targetType\":\"PANGU\",\n"
        jsonstring += "\t\"targetDetail\":\n"
        jsonstring += "\t\"{\n"
        jsonstring += "\t\t\\\"Path\\\":\\\"pangu://%s:%s%s\\\",\n" % (self.destnuwa, self.nuwa_port, destdir)
        jsonstring += "\t\t\\\"Capability\\\":\\\"%s\\\"\n" % (self.destcap)
        jsonstring += "\t}\"\n"
        jsonstring += "}\n"

        return jsonstring 

    def buildStonehengeList(self, fileName):
        stonehengeList = ''
        for path in file(fileName).readlines():
            path = path.strip()
            stonehengeList += self.buildOneStongehenge(path, path)
        return stonehengeList 
    
    def makeStonehenge(self, srcdir, destdir):
        jsonstring = ''
        if destdir == '':
            jsonstring = self.buildStonehengeList(srcdir)
        else:
            jsonstring = self.buildOneStongehenge(srcdir, destdir)
        stone = open(self.stonehenge_path, 'w')
        stone.write(jsonstring)
        stone.close()

class YishanJob:
    def __init__(self,clusterConfPath=None):
        self.configer = YishanConfig(clusterConfPath)
        self.filelogname = '/tmp/shenzhou_%s.log'%(time.strftime("%Y-%m-%d",time.localtime()))
        self.isGo = True
        #remove package
        Package('aos_yugong2', 'remove')
        #add package
        Package('aos_yugong2', 'add')
         
    def cleanup(self):
        print '[yishan2]: clean up'
        if ys.configer.type == "pangu2pangu":
            if GetClusterName('localcluster') == GetClusterName(self.configer.srcnuwa):
                self.configer.nuwa_addr = self.configer.srcnuwa
            elif GetClusterName('localcluster') == GetClusterName(self.configer.destnuwa):
                self.configer.nuwa_addr = self.configer.destnuwa
            else:
                return -2
        else:
            self.configer.nuwa_addr = self.configer.destnuwa
#remove old ys job
        stopJobCMD = RPC_CALLER + " --Server=nuwa://%s:%s/sys/fuxi/master/ForChildMaster --Method=StopWorkItem --Parameter=nuwa://%s:%s/%s/%s/JobMaster &>/dev/null" %(self.configer.nuwa_addr, self.configer.nuwa_port, self.configer.nuwa_addr, self.configer.nuwa_port, self.configer.job_user, self.configer.job_name)
        rmTmpCMD = "echo y|" + PU + " rmdir pangu://%s:%s/tmp/%s/ &>/dev/null" %(self.configer.nuwa_addr, self.configer.nuwa_port, self.configer.job_user)
        os.system(stopJobCMD)
        os.system(rmTmpCMD)
         
    def transfer(self, toboat = 0, shenzhou=''):
        isSuceess = False
        print '[yishan2]: transfer start'
        writeLog(self.filelogname, '[yishan2]: transfer start\n')
        if ys.configer.type == "pangu2pangu":
            if GetClusterName('localcluster') == GetClusterName(self.configer.srcnuwa):
                self.configer.nuwa_addr = self.configer.srcnuwa
            elif GetClusterName('localcluster') == GetClusterName(self.configer.destnuwa):
                self.configer.nuwa_addr = self.configer.destnuwa
            else:
                return -2
        else:
            self.configer.nuwa_addr = self.configer.destnuwa
            
        if self.configer.production == 'yes':
            capabilityfile = '/apsara/security/internal_capability/InternalCapabilityForYu.txt'
        elif self.configer.production == 'no':
            capabilityfile = '/apsara/deploy/InternalCapabilityForYu.txt'
        else:
            return -2
            
        if self.configer.pangu_mode == '-1':
            yuCMD = "%s/yu2 --CapabilityFile=%s --yugong_TempFileCount=%s --yugong_NuwaHost=%s:%s --yugong_JavaHome=%s/jre --yugong_JavaPlatform=amd64 --yugong_FuxiUser=%s --yugong_FuxiJobName=%s --yugong_CopyBufferSize=%s" %(self.configer.yu2_home, capabilityfile, self.configer.instance_num, self.configer.nuwa_addr, self.configer.nuwa_port, self.configer.jre_home, self.configer.job_user, self.configer.job_name, self.configer.buffer_size)
        else:
            yuCMD = "%s/yu2 --CapabilityFile=%s --yugong_TempFileCount=%s --yugong_NuwaHost=%s:%s --yugong_JavaHome=%s/jre --yugong_JavaPlatform=amd64 --yugong_FuxiUser=%s --yugong_FuxiJobName=%s --yugong_CopyBufferSize=%s --yugong_PanguFileFlag=%s" %(self.configer.yu2_home, capabilityfile, self.configer.instance_num, self.configer.nuwa_addr, self.configer.nuwa_port, self.configer.jre_home, self.configer.job_user, self.configer.job_name, self.configer.buffer_size, self.configer.pangu_mode)
        if self.configer.keeptempfile == 'yes':
            yuCMD = yuCMD + " --yugong_KeepTempFileIfFailure"
        yuCMD = yuCMD + " --yugong_MinMinCopy=2 --yugong_MinMaxCopy=2"
        print yuCMD
        writeLog(self.filelogname, yuCMD+'\n')
        alertWarning('ok', 'yishan start now....') 
        if int(toboat) == 0:
            ret = os.system(yuCMD)
            print '[yishan2]: transfer complete: ' + str(ret == 0)
            return ret == 0
        else:
            logdata = shenzhou.makeLogData('2','o')
            result = shenzhou.logYuGong(logdata)
            if result == False:
                alertWarning('error', 'writing dmp_yugong_log error!')
                sys.exit(1)
            elif shenzhou.log_id == '':
                shenzhou.log_id = result
            else:
                pass
            i = subprocess.Popen(args=yuCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            while(self.isGo):
                try:
                    thread_error = threading.Thread(target=self.checkError,args=(i,shenzhou))
                    thread_error.start()
                    thread_error.join()
                    if self.isGo == False:
                        sys.exit(1)
                    out=i.stdout.readline(512)
                    writeLog(self.filelogname, out+'\n')
                    if out.find('Total') != -1:
                        print out
                    if out.find('Prepare') != -1:
                        print out
                    if out.find('AccessName') != -1:
                        print out
                    intStart = out.rfind('copied')
                    intEnd = out.rfind('%')
                    bytestart = out.rfind('copy, ')
                    shenzhou.byte = out[int(bytestart)+6:int(intStart)-1]
                    intDegree = 0
                    if intStart != -1 and intEnd != -1:
                        intDegree = out[int(intStart)+6:int(intEnd)+1]
                    if intDegree == '' or intDegree == 0:
                        continue
                    print "copied:"+intDegree+"....."
                    logdata = shenzhou.makeLogData('2', intDegree)
                    result = shenzhou.logYuGong(logdata)
                    if 'Failed' in out:
                        ret = 1
                        break
                    if 'Terminated' in out:
                        ret = 0
                        logdata = shenzhou.makeLogData('1', intDegree)
                        result = shenzhou.logYuGong(logdata)
                        shenzhou.registerFile()
                        alertWarning('ok', 'yishan running success!')
                        break
                    nowtime = time.strftime("%H:%M:%S", time.localtime())
                    if nowtime >= '22:50:00':
                        alertWarning('warning', 'yishan running timeout')
                        logdata = shenzhou.makeLogData('3', intDegree)
                        result = shenzhou.logYuGong(logdata)
                        writeLog(self.filelogname, 'yishan timeout\n')
                        sys.exit(1)
                    time.sleep(5)
                except KeyboardInterrupt:
                    print 'yishan has terminated by keyboardInterrrupt\n'
                    print '[yishan2]: transfer false'
                    logdata = shenzhou.makeLogData('3', 'o')
                    result = shenzhou.logYuGong(logdata)
                    alertWarning('critical', 'yishan keyboardInterrupt!')
                    sys.exit(1)  
        print '[yishan2]: transfer complete: ' + str(ret == 0)
        writeLog(self.filelogname, '[yishan2]: transfer complete: ' + str(ret == 0)+'\n')
        return ret == 0

    def checkError(self, process, shenzhou):
        error = process.stderr.readline()
        if len(error) > 0:
            print error
            logdata = shenzhou.makeLogData('3', 'o')
            result = shenzhou.logYuGong(logdata)
            alertWarning('critical', error)
            self.isGo = False
            sys.exit(1)
  
    def moniter(self, times, ret, toboat, shenzhou=''):
        retry_num = times
        if retry_num <= 0 or ret:
            if retry_num == 0 and toboat != 0 and ret == False:
                logdata = shenzhou.makeLogData('3', 'o')
                result = shenzhou.logYuGong(logdata)
                send_mail('mail.tpl')
                alertWarning('critical', 'yugong job failed!')
                writeLog(self.filelogname, 'yugong job failed\n')
            return 0
        while(True):
            print '[yishan2]: yugong job Failed'
            writeLog(self.filelogname, '[yishan2]: yugong job Failed\n')
            if retry_num == 0:
                print '[yishan2]: Reach max retry time. Failed to transfer.'
#failed log
                if toboat != 0:
                    logdata = shenzhou.makeLogData('3', 'o')
                    result = shenzhou.logYuGong(logdata)
#end failed log
                send_mail('mail.tpl')
                alertWarning('critical', 'yugong job failed!')
                sys.exit(1)
            print '[yishan2]: Retry ' + str(retry_num) + ' times'
            writeLog(self.filelogname, '[yishan2]: Retry ' + str(retry_num) + ' times\n')
            if retry_num <= 2:
                alertWarning('warning', 'yugong job retry last %s times'%(retry_num))
            self.cleanup()
            ret = self.transfer(toboat, shenzhou)
            if ret:
                print '[yishan2]: yugong job success'
                alertWarning('ok', 'yugong job success and finish!')
                break
            retry_num = retry_num - 1
            time.sleep(90)

# check input is not null
not_null = lambda v:v and len(v)>0

def CheckPmRun(str):
    key = 'error: [NA]'
    pos = str.find(key)
    if pos > 0:
        return True
    else:
        return  False

def Package(packagename, method):
        if method == 'add':
            packagepath = PACKAGEPATH + packagename + "_" + ARCH + "_" + VERSION + ".tar.gz"
            cmdline = PM_RUN + ' -t -pm localcluster:10240 AddPackage package://%s  %s  %s' % (packagename, packagename, packagepath)
            ret = os.popen(cmdline).read()
        else:
            cmdline = PM_RUN + ' -t -pm localcluster:10240 RemovePackage package://%s' % (packagename)
            ret = os.popen(cmdline).read()
        if CheckPmRun(ret):
            print "package %s %s success" % (packagename, method)
        else:
            print "package %s %s failed" % (packagename, method)
        if method == 'add' and not CheckPmRun(ret):
            sys.exit(1)

def GetClusterName(nuwa):
    if nuwa == 'localcluster':
        cmd = '/bin/me 2>&1'
    else:
        cmd = '/bin/me 2>&1 --ip %s' % nuwa
    print cmd
    ret = os.popen(cmd).read()
    print ret
    p = re.compile('clusterName_([a-z\-A-Z0-9\.\-]*)')
    clustername = p.search(ret).group(1)
    return clustername

def GetProduction():
    clustername=GetClusterName('localcluster')
    cmd = '/bin/me --get %s_production' % clustername
    return os.popen(cmd).read().strip()


def get_prompt(msg, default=None, func=not_null):
    if default:
        msg += ", default: %s" % default
    msg   = "[%s] " % msg
    value = raw_input(msg) or default
    # no input for loop
    while not func(value):
        value = raw_input(msg) or default
    return value

def usage():
    print ''' 
    usage: yishan2.py [-r retry_times] [-h] [-d parent_dest_dir] <file1,file2...>
        -r retry_times   if transfer failed, yishan will retry n times. default 0
        -s src_path copy src path. for example: yishan2.py -s /a/
        -d dest_dir copy dest dir.for example: yishan2.py -d /b/
        yishan2.py -s /a/ -d /b/ means copy src cluster /a/ to dest cluster /b/
        -h help
        -t transfer to shenzhou
        -m delete pangu file

        Note if -d is not specified, src_path is supposed to be a list of files:
        like file1,file2... means a src file list(full path, without header, 
        etc: pangu:// ) and the files will copy to the same path in destination 

        changelist:
             1. add pangu 2 pangu support
             2. add pangu mode support (16 means compress)
             3. add nuwa_mode so that yishan2 can both run in src cluster or dest cluster
          '''
if __name__=='__main__':
    try:
        retry_num = 0
        srcdir = ''
        destdir = ''
        toboat = 0
        deletefile = ''
        confdir = None
        opts,args=getopt.getopt(sys.argv[1:],'hr:s:d:tm:c:', ['help', 'retry', 'src', 'dest', 'toboat','mvfile','confdir'])
        for opt,arg in opts:
            if opt in ("-h","--help"):
                usage()
                sys.exit(1)
            elif opt in ('-r', '--retry'):
                if arg > 0:
                    retry_num = int(arg)
            elif opt in ('-s', '--src'):
                if arg > 0:
                    srcdir = arg
            elif opt in ('-d', '--dest'):
                if arg > 0:
                    destdir = arg
            elif opt in ('-t', '--toboat'):
                if arg > 0:
                    toboat = 1
            elif opt in ('-m', '--mvfile'):
                if arg > 0:
                    deletefile = arg
            elif opt in ('-c', '--confdir'):
                if arg > 0:
                    confdir = arg
            else:
                usage()
                sys.exit(1)
        if (deletefile == '' and srcdir == ''):
            usage()
            sys.exit(1)
        ys = YishanJob(confdir)
        if deletefile != '':
            shenzhou = ShenZhou(deletefile,'') 
            shenzhou.deleteFile(deletefile)
            sys.exit(1)
        print "now transfer mode is %s" % ys.configer.type
        if ys.configer.type == "hdfs2pangu":
            print "soucre hadoop namenode ip is %s" % ys.configer.namenode
            print "dest nuwa ip is %s" % ys.configer.destnuwa
        elif ys.configer.type == "pangu2pangu":
            print "source cluster is %s" % GetClusterName(ys.configer.srcnuwa)
            print "dest nuwa ip is %s" % GetClusterName(ys.configer.destnuwa)
        else:
            print "not support this mode %s " % ys.configer.type
            sys.exit()
        print "start yishan2.conf"
        ys.cleanup()
        ret = ys.configer.makeStonehenge(srcdir, destdir)
        if ret == -1:
            print '[yishan2]: not support transfer type'
            sys.exit(1)
        elif ret == -2:
            print '[yishan2]: only supprot src/dest in nuwa mode:src mean run yishan2 in src cluster,dest mean run yishan2 in dest cluster'
            sys.exit()
        if toboat == 0:
            ret = ys.transfer(toboat)
            ys.moniter(retry_num, ret, toboat)
        else:
            ret = ys.transfer(toboat, shenzhou)
            ys.moniter(retry_num, ret, toboat, shenzhou)

        if not ret:
            sys.exit(1)
    except getopt.GetoptError:
        usage()
        sys.exit(1)
