#! /usr/bin/env python

import os, re, sys
import subprocess
import process
import logging
import log
import process_multiple
import pdb
import simplejson

from configuration import Configuration


class Ha2Tool:
    def __init__(self, pgRoot,configPath,toolPath):
        self.toolPath   = toolPath
        self.ha2Cmd     = self.toolPath + '/ha2'
        self.queryCmd   = self.toolPath + '/search_query.sh'
        self.ha2Conf    = self.toolPath + '/tools.conf'
        self.pgAddr     = pgRoot

        p=re.compile('pangu://(.*):10240')
        if p.match(pgRoot):
            self.nuwaIP = p.search(pgRoot).groups(1)[0]
        else:
            print "Can't resolve nuwaIp adress"
            sys.exit(1)
        self.confDir    = configPath
        self.logger     = logging.getLogger()

    def invoke(self, cmd, timeout = 0):
        p = process.Process(cmd)
        code, data, error = p.run(timeout)
        return code, data, error

    def simpleInvoke(self, cmd, timeout = 0):
        p = process.Process(cmd)
        rst = p.runInConsole(timeout)
        return rst

    def multInvoke(self,cmd,timeout = 0):
        p = process_multiple.Process_multiple(cmd)
        rst = p.run_multresout(timeout)
        return rst

    def invoke2(self, cmd, timeout = 0):
        p = process.Process(cmd)
        return p.runWithoutPipe(timeout)
    
    def deployConfiguration(self, serviceName,timeout = 0):
        cmd = self.ha2Cmd + ' dp -p %s%s -l %s -c %s' % (self.pgAddr,serviceName,self.confDir,self.ha2Conf)
        (retcode, stdout, stderr) = self.invoke(cmd, timeout)

        if retcode != 0:
            self.logger.error('deploy config error,pangu:[%s%s] config: [%s] err:[%s]' % \
                              (self.pgAddr,serviceName,self.ha2Conf, stdout + stderr))
            return False
        return True

    def switchIndex(self,serviceName,cluster,timeout = 0):
        cmd = self.ha2Cmd + ' swi -p %s%s/ --cluster_name=%s -c %s' % (self.pgAddr,serviceName,cluster,self.ha2Conf)

        (retcode, stdout, stderr) = self.invoke(cmd, timeout)
        if retcode != 0:
            self.logger.error('switch index error,pangu:[%s] config: [%s] err:[%s]' % \
                              (self.pgAddr,self.ha2Conf, stdout + stderr))
            return False
        return True

    def startService(self,serviceName, timeout = 0):
        cmd = self.ha2Cmd + ' sts -p %s%s -c %s' % (self.pgAddr,serviceName,self.ha2Conf)
        retcode, stdout, stderr = self.invoke(cmd, timeout)
        if retcode != 0:
            self.logger.error('start %s service fail:pangu:[%s] config: [%s] err:[%s]' % \
                                  (serviceName,self.pgAddr,self.ha2Conf,stdout+stderr))
            return None
        return serviceName

    def stopService(self,serviceName, timeout = 0):
        cmd = self.ha2Cmd + ' sps -p %s%s -c %s' % (self.pgAddr,serviceName,self.ha2Conf)
        retcode, stdout, stderr = self.invoke(cmd, timeout)
        if retcode != 0:
            self.logger.error('stop %s service fail:pangu:[%s] config: [%s] err:[%s]' % \
                                  (serviceName,self.pgAddr,self.ha2Conf,stdout+stderr))
            return False
        return True

    def stopIncrBuildJob(self,serviceName, clusterName, timeout = 0):
        cmd = self.ha2Cmd + ' bi -p %s%s -n %s -c %s -s stop' % (self.pgAddr,serviceName, clusterName, self.ha2Conf)
        retcode, stdout, stderr = self.invoke(cmd, timeout)
        return True

    def buildIndex(self,serviceName, cluster, mode, filepattern, timeout = 0):
        cmd = self.ha2Cmd + ' bi -m %s -p %s%s -c %s -n %s -i "' % (mode, self.pgAddr, serviceName,self.ha2Conf, cluster)
        for i in filepattern:
            cmd += i+';'
        cmd += '"'

        self.logger.info(cmd)
        retcode, stdout, stderr = self.invoke(cmd, timeout)
        if retcode != 0:
            self.logger.error('build %s index fail:pangu:[%s] cluster:[%s] config: [%s] mode[%s] filepattern[%s] err:[%s]' % \
                                  (serviceName,self.pgAddr,cluster,self.ha2Conf,mode,filepattern,stdout+stderr))
            return False
        return True

    def getIncrBuildStatusStr(self, serviceName, clusterName, timeout = 0):
        cmd = self.ha2Cmd + ' bi -p %s%s -c %s -n %s -s getstatus' % (self.pgAddr,serviceName, self.ha2Conf,clusterName)
        retcode, stdout, stderr = self.invoke(cmd, timeout)
        if retcode != 0:
            self.logger.error('get increase build status error: [%s]' % cmd)
            return ""
        #self.logger.debug('stdout: ' + stdout)
        pos = stdout.find('buildstatus=')
        if pos == -1:
            return ""
        return stdout[pos+12:-14]


    def getIncrBuildStatus(self,serviceName,clusterName,config=Configuration(),timeout = 0):
        statusStr = self.getIncrBuildStatusStr(serviceName,clusterName)
        if len(statusStr) == 0:
            return None

        statusJson = simplejson.loads(statusStr)
        return statusJson['BuildPhase']

    def getServiceStatusOK(self,serviceName, timeout=0 ):
        cmd = self.ha2Cmd + ' gs -p %s%s -c %s' % (self.pgAddr,serviceName,self.ha2Conf)
        retcode, stdout, stderr = self.invoke(cmd, timeout)
        if retcode !=0:
            self.logger.error('get service status failed :pangu:[%s] config: [%s] err:[%s]' % \
                                  (self.pgAddr,self.ha2Conf,stdout+stderr))
            return False
        return True

    def searchQuery(self,serviceName, clusterName, query, timeout = 0):
        queryString = 'config=cluster:%s&&query=phrase:%s' % (clusterName, query)
        
        cmd = self.queryCmd + ' %s  %s  admin "%s"' % (serviceName,self.nuwaIP, queryString)
        (retcode, stdout, stderr) = self.invoke2(cmd, timeout)
        if retcode != 0:
            self.logger.error('search query error: [%s], [%s]' % \
                                  (queryString, stdout + stderr))
            return None
        else:
            return stdout
        

    def searchQueryStr(self,serviceName, queryStr, timeout = 0):
        queryString = queryStr
        cmd = self.queryCmd + ' %s  %s  admin "%s"' % (serviceName,self.nuwaIP, queryString)
        (retcode, stdout, stderr) = self.invoke2(cmd, timeout)
        if retcode != 0:
            self.logger.error('search query error: [%s], [%s]' % \
                                  (queryString, stdout + stderr))
            return None
        else:
            return stdout
        

    def getClusterStatusStr(self, serviceName, timeout = 0):
        cmd = self.ha2Cmd + ' gs -p %s%s -c %s' % (self.pgAddr,serviceName,self.ha2Conf)
        retcode, stdout, stderr = self.invoke(cmd, timeout)
        if retcode != 0:
            self.logger.error('get cluster status error: [%s]' % cmd)
            return ""
        #self.logger.debug('stdout: ' + stdout)
        pos = stdout.find('TraceLogLevel=ALL')
        if pos == -1:
            return ""
        return stdout[pos+18:-15]


    def getClusterStatus(self,serviceName,config=Configuration(),timeout = 0):
        statusStr = self.getClusterStatusStr(serviceName)
        if len(statusStr) == 0:
            return None

        statusJson = simplejson.loads(statusStr)

        for cluster in config.services[serviceName]:
            k = statusJson['multi_version_cluster_info'][cluster]['cluster_info_map'].keys()[0]
            leftNum,righNum = statusJson['multi_version_cluster_info'][cluster]['cluster_info_map'][k]['searcher_load_completed'].split('/')
            if leftNum < righNum:
                return 'loading'

        return 'loaddone'


if __name__ == '__main__':

    ha2 = Ha2Tool('pangu://10.249.49.2:10240/home/admin/daogou/','/apsarapangu/disk5/daogou/crontab/pe_code/index_switcher/ay33_kuafu2','/apsarapangu/disk5/daogou/crontab/pe_code/index_switcher/console')
    ret = ha2.getServiceStatusOK('daogou_combo')
