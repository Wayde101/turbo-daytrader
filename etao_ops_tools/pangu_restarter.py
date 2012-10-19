#! /usr/bin/env python

import subprocess
import time
import re
import os
import sys
import socket

class Process:
    GlobalTimeout = 0
    intervalSecond = 1

    def __init__(self, cmd):
        self.cmd = cmd

    def runInConsole(self, timeout = GlobalTimeout):
        p = subprocess.Popen(self.cmd, shell=True)
        if timeout > 0:
            self.wait(p, timeout)
        p.wait()
        return p.returncode

    def run(self):
        print self.cmd
        tmpOutFile = '.process_run_out'
        tmpErrFile = '.process_run_err'
        self.cmd = self.cmd + ' >' + tmpOutFile +  ' 2>' + tmpErrFile
        retcode = self.runInConsole()

        stdout = stderr = ''
        if os.path.exists(tmpOutFile):
            stdout = file(tmpOutFile).read()
        if os.path.exists(tmpErrFile):
            stderr = file(tmpErrFile).read()
        return retcode, stdout, stderr


class RpcCallerWrapper:
    def __init__(self, executable = '/apsara/deploy/rpc_caller'):
        self.executable = executable

    def invoke(self, cmd):
        p = Process(cmd)
        return p.run()

    def call(self, server, method, parameter):
        cmd = '%s --Server=%s --Method=%s --Parameter=%s' % \
            (self.executable, server, method, parameter)
        retcode, stdout, stderr = self.invoke(cmd)
        print 'out: ' + (stdout + stderr)
        if retcode != 0:
            return None
        return stdout

    def call2(self, server, method, parameterFile):
        cmd = '%s --Server=%s --Method=%s --ParameterFile=%s' % \
            (self.executable, server, method, parameterFile)
        retcode, stdout, stderr = self.invoke(cmd)
        print 'out: ' + (stdout + stderr)
        if retcode != 0:
            return None
        return stdout

class FuxiMasterWrapper:
    def __init__(self, nuwaAddr = None, rpcCallerBin = '/apsara/deploy/rpc_caller'):
        if nuwaAddr == None:
            nuwaAddr = "nuwa://localcluster"
        self.forChildMaster = nuwaAddr + '/sys/fuxi/master/ForChildMaster'
        self.rpcCaller = RpcCallerWrapper(rpcCallerBin)
    
    def getWorkItemStatus(self, accessName):
        method = 'GetWorkItemStatus'
        stdout = self.rpcCaller.call(self.forChildMaster, method, accessName)
        if stdout == None:
            return None
        pos = stdout.find('Return=')
        if pos == -1:
            return None
        return stdout[pos + 7:].strip()

    #return accessName
    def startWorkItem(self, jsonFile):
        method = "StartWorkItem"
        stdout = self.rpcCaller.call2(self.forChildMaster, method, jsonFile)
        if stdout == None:
            return None
        pos = stdout.find('Return=')
        if pos == -1:
            return None
        pattern = re.compile('"AccessName"\s*:\s*"(.*?)"')
        match = re.search(pattern, stdout)
        if match != None:
            return match.group(1)
        return None

    def stopWorkItem(self, accessName):
        method = "StopWorkItem"
        stdout = self.rpcCaller.call(self.forChildMaster, method, accessName)
        print stdout
        if stdout == None:
            return False

        notFoundPattern = re.compile('workitem\s+not\s+found', re.IGNORECASE)
        if re.search(notFoundPattern, stdout):
            print 'not found work item [%s]' % accessName
            return True

        pos = stdout.find('Return=')
        if pos == -1:
            return False
        ack = stdout[pos + 7:].strip()
        if ack.upper() == 'OK':
            return True
        return False


class PuWrapper:
    def __init__(self, executable='/apsara/deploy/pu'):
        self.executable = executable

    def copyFromLocal(self, localFile, panguFile):
        cmd = '%s cp %s %s' % (self.executable, localFile, panguFile)
        p = Process(cmd)
        retcode, stdout, stderr = p.run()
        if retcode != 0:
            return False
        if stdout.find('1 file copied') == -1:
            return False
        return True

    def removeFile(self, panguFile):
        cmd = '%s rm %s' % (self.executable, panguFile)
        p = Process(cmd)
        retcode, stdout, stderr = p.run()
        if retcode != 0:
            return False
        if len(stdout) == 0 and len(stderr) == 0:
            return True
        return False


class PuadminWrapper:
    def __init__(self, executable = '/apsara/deploy/puadmin'):
        self.executable = executable
    
    def lscs(self, puAddress):
        cmd = '%s lsCS %s' % (self.executable, puAddress)
        p = Process(cmd)
        retcode, stdout, stderr = p.run()
        if retcode != 0:
            return None

        errorPattern = 'Exception'
        if stdout.find(errorPattern) != -1 or \
                stderr.find(errorPattern) != -1:
            return None

        normalCSList = list()
        unnormalCSList = list()
        totalDiskSize = totalFileSize = totalDiskSize = 0
        pattern = re.compile('[\d]+\.\s+([A-Z]+).*ChunkServerRole/(.*)')
        for line in re.split('\n', stdout):
            match = pattern.match(line.strip())
            if match != None:
                if match.group(1).upper() == 'NORMAL':
                    normalCSList.append(match.group(2))
                else:
                    unnormalCSList.append(match.group(2))
        print str(normalCSList)
        print str(unnormalCSList)
        return normalCSList, unnormalCSList

class PanguRestarter:
    def __init__(self, clusterNuwa, jsonFile, maxUnnormalCSNum):
        self.clusterNuwa = clusterNuwa
        self.jsonFile = jsonFile
        self.panguMaster = clusterNuwa + '/sys/pangu/master'
        self.maxUnnormalCSNum = maxUnnormalCSNum
        self.panguAccessName = None
    
    def stopPangu(self):
        self.panguAccessName = self.clusterNuwa + '/sys/pangu/ServiceMaster'
        fuxiMaster = FuxiMasterWrapper(self.clusterNuwa)
        if not fuxiMaster.stopWorkItem(self.panguAccessName):
            return False

        puadminWrapper = PuadminWrapper()
        while True:
            status = puadminWrapper.lscs(self.panguMaster)
            if status == None:
                break
            time.sleep(10)

        self.panguAccessName = None
        return True

    def getNuwaAddress(self, panguAccessName):
        match = re.compile('nuwa://([^/]+)/').match(panguAccessName)
        if match == None:
            raise ValueError, 'pangu access name invalid: [%s]' % panguAccessName
        return match.group(1)

    def checkPanguReady(self):
        if self.panguAccessName == None:
            raise ValueError, 'panguAccessName is None'
        puadminWrapper = PuadminWrapper()
        status = puadminWrapper.lscs(self.panguMaster)
        if status == None:
            return False

        unnormalCSList = status[1]
        if len(unnormalCSList) > self.maxUnnormalCSNum:
            return False

        nuwaAddress = self.getNuwaAddress(self.panguAccessName)
        puWrapper = PuWrapper()
        localFile = __file__
        fileName = os.path.basename(localFile)
        fileName = fileName + str(time.time())
        panguFile = 'pangu://' + nuwaAddress + '/' + fileName
        if not puWrapper.copyFromLocal(localFile, panguFile):
            print 'copy fro local failed'
            return False
        if not puWrapper.removeFile(panguFile):
            print 'remove file failed'
            return False
        return True

    def startPangu(self):
        if self.panguAccessName != None:
            raise ValueError, 'please stop pangu first'

        fuxiMaster = FuxiMasterWrapper(self.clusterNuwa)
        self.panguAccessName = fuxiMaster.startWorkItem(self.jsonFile)
        if self.panguAccessName == None:
            return False

        self.panguAccessName = self.panguAccessName.replace('\\', '')
        print self.panguAccessName
        while True:
            if self.checkPanguReady():
                break;
            print 'sleep 10s ...'
            time.sleep(30)
        return True
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >> sys.stderr, 'Usage: %s max-unnormal-chunkserver-num' % sys.argv[0]
        sys.exit(1)

    try :
        maxUnnormalCSNum = int(sys.argv[1])
    except TypeError, e:
        print >> sys.stderr, 'max-unnormal-chunkserver-num must be a num'
        sys.exit(1)

    jsonFile = '/apsara/deploy/package/pangu.json'
    nuwaHost = 'localcluster'

    if not os.path.exists(jsonFile):
        print >>sys.stderr, 'file [%s] not exists'
        sys.exit(1)

    try:
        nuwaIp = socket.gethostbyname(nuwaHost)
    except Exception, e:
        print >> sys.stderr, 'Error: parse host name failed: [%s]' % nuwaHost
        sys.exit(1)

    nuwaAddress = 'nuwa://' + nuwaIp + ':10240'
    panguRestarter = PanguRestarter(nuwaAddress, jsonFile, maxUnnormalCSNum)
    print 'stop pangu ...'
    if not panguRestarter.stopPangu():
        print 'stop pangu failed'
        sys.exit(1)

    print 'sleep 10 s...'
    time.sleep(10)
    print 'start pangu...'
    if not panguRestarter.startPangu():
        print 'start pangu failed'
        sys.exit(1)
    print 'start pangu success'
    sys.exit(0)


