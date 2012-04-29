#! /usr/bin/env python

import sys, os, re
import time
import logging
import log
import util

from configuration import Configuration
from ha2_configuration import Ha2Configuration
from nuwa_console_wrapper import NuwaConsoleWrapper
from abench_wrapper import AbenchWrapper

class ClusterWarmer:
    def __init__(self, configRoot, config = Configuration()):
        self.configuration = config
        self.configRoot = configRoot
        self.logger = logging.getLogger()

    def getQrsAddressList(self, configPath):
        ha2Configuration = Ha2Configuration(configPath)
        qrsRoot = ha2Configuration.getQrsAddress()
        nuwaConsole = NuwaConsoleWrapper(self.configuration.nuwaConsoleBin)
        cmdTimeout = self.configuration.commandTimeout
        return nuwaConsole.listDirectory(qrsRoot, cmdTimeout)

    def getQueryLogPath(self, queryPath):
        if os.path.isabs(queryPath):
            return queryPath
        
        currPath = os.path.dirname(__file__)
        queryLogRoot = os.path.join(currPath, '../query_log/')
        return os.path.join(queryLogRoot, queryPath)

    def startAbench(self, threadNum = 20, timeLen = 1200):
        queryPathList = list()
        qrsList = list()

        for serviceName in self.configuration.services:
            configPath = util.getConfigPath(serviceName)
            configPath = os.path.join(self.configRoot, configPath)
                        
            currQrsList = self.getQrsAddressList(configPath)
            self.logger.debug('qrs addresses: ' + str(currQrsList))
            if currQrsList == None:
                self.logger.error('get qrs address list error')
                return False
            
            qrsRoot = Ha2Configuration(configPath).getQrsAddress()
            ha2Configuration = Ha2Configuration(configPath)
            clusterNames = ha2Configuration.getServiceClusters()
            qrsIndex = 0
            for clusterName in clusterNames:
                queryPath = self.configuration.queryLogMap[clusterName]
                queryPath = self.getQueryLogPath(queryPath)
                queryPathList.append(queryPath)
                
                qrsList.append(qrsRoot + '/' + currQrsList[qrsIndex])
                qrsIndex = (qrsIndex + 1) % len(clusterNames)
        
        abenchWrapper = AbenchWrapper(self.configuration.abenchBin)
        if not abenchWrapper.startMultiAbench(queryPathList, qrsList, \
                                              threadNum, timeLen):
            self.logger.error('cluster warmup failed')
            return False
        return True
        

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s config-root' % sys.argv[0]
        sys.exit(1)

    configRoot = sys.argv[1]
    clusterWarmer = ClusterWarmer(configRoot)
    clusterWarmer.startAbench(timeLen = 10)
