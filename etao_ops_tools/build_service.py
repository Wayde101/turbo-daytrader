#! /usr/bin/env python

import os, sys
import time
import logging
import log
import error

from configuration import Configuration
from ha2_tool import Ha2Tool


class BuildService:
    intervalSecond = 10

    def __init__(self, pgRoot, configPath,  configuration = Configuration(), serviceName = '', clusterName = ''):
        self.configPath = configPath

        self.configuration = configuration
        self.ha2ToolPath = configuration.ha2ToolPath
        self.ha2Tool = Ha2Tool(pgRoot,configPath,self.ha2ToolPath)
        self.serviceName = serviceName
        self.clusterName = clusterName

        self.logger = logging.getLogger()
        self.noData = True

    def setNoData(self, nodata = False):
        self.noData = nodata

    #build increase index
    def buildIncrIndex(self, filepatten, timeout = 0):
        self.logger.info('stop build increase job')
        for i in range(3):
            if not self.ha2Tool.stopIncrBuildJob(self.serviceName, self.clusterName):
                self.logger.error("stop increase build job error")
                return error.ERROR_STOP_BUILD_JOB
            time.sleep(30)

        self.logger.info('build increase index: [%s]' % filepatten)
        if not self.ha2Tool.buildIndex(self.serviceName, self.clusterName, 'i', filepatten):
            self.logger.error(("start increase build job error: serviceName:[%s] clusterName:[%s] mode:[%s] filepattern:[%s]") % self.serviceName, self.clustername, 'i', filepatten)
            return error.ERROR_BUILD_INCR_INDEX

        startTime = time.time()   
        self.logger.info('wait for build increase job start')
        statusStr = self.ha2Tool.getIncrBuildStatus(self.serviceName, self.clusterName)
        self.logger.info(('job status: [%s]') % statusStr)
        #it is start successed when STATUS is not BuildStoped
        while statusStr == 'BuildStopped':
            currTime = time.time()
            if timeout != 0 and startTime + timeout < currTime:
                self.logger.error("start build increase job timeout")
                return error.ERROR_BUILD_INCR_INDEX

            time.sleep(5)
            statusStr = self.ha2Tool.getIncrBuildStatus(self.serviceName, self.clusterName)
            self.logger.info(('job status: [%s]') % statusStr)

        self.logger.info('build increase job started')
        return error.NO_ERROR

    def waitBuildIncrIndex(self, timeout = 0):
        self.logger.info('wait for build increase job complete')

        if (self.noData):
            self.logger.info('return immediately, the data is null')
            return error.NO_ERROR

        startTime = time.time()   
        statusStr = self.ha2Tool.getIncrBuildStatus(self.serviceName, self.clusterName)
        self.logger.info(('job status: [%s]') % statusStr)
        #it is start successed when STATUS is not BuildStoped
        while statusStr != 'BuildStopped':
            currTime = time.time()
            if timeout != 0 and startTime + timeout < currTime:
                self.logger.error("wait for build increase job timeout")
                return error.ERROR_BUILD_INCR_INDEX

            time.sleep(5)
            statusStr = self.ha2Tool.getIncrBuildStatus(self.serviceName, self.clusterName)
            self.logger.info(('job status: [%s]') % statusStr)

        if not self.ha2Tool.stopIncrBuildJob(self.serviceName, self.clusterName):
            self.logger.error("stop increase build job error")
            return error.ERROR_STOP_BUILD_JOB

        self.logger.info('build increase job completed')
        return error.NO_ERROR

def printUsage():
    print >> sys.stderr, sys.argv[0], ' <serivce-local-root> <filepatten>'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        printUsage()
        sys.exit(1)

    configPath = sys.argv[1]
    filepatten = []
    filepatten.append(sys.argv[2])
    buildService = BuildService(configPath, Configuration(), 'daogou_combo', 'daogou_luntan')
    buildService.buildIncrIndex(filepatten)

