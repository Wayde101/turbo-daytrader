#! /usr/bin/env python
import os, sys, re, time
import pickle
import logging
import configuration
import util
import error

from optparse import OptionParser
from hadoop_tool import HadoopTool
from search_system import SearchSystem
from pangu_wrapper import PanguWrapper

class Controller:
    def __init__(self, configuration = configuration.Configuration()):
        self.config = configuration
        hadoop_client_path = 'hadoop_client/bin'
        self.doneFile =  configuration.doneFile
        self.copyingFile =configuration.copyingFile

        hadoopToolPath = os.path.join(os.path.dirname(__file__),hadoop_client_path)
        self.hadoopRoot = configuration.hadoopDumpRoot
        self.panguRoot = configuration.panguDataRoot

        self.hadoopWrapper = HadoopTool(hadoopToolPath)
        self.pangWrapper   = PanguWrapper()
        path = 'dump%s' % time.strftime('%Y-%m-%d',time.localtime())
        self.panguRoot = util.joinPanguPath(self.panguRoot, path)
        self.eagleLogFile = configuration.eagleLogFile
        self.jobIds = None
        self.logger = logging.getLogger()

        self.searchSystem=SearchSystem(self.config)

    def printLog(self, info):
        fobj = open(self.eagleLogFile, 'a')
        info = info + ' ' + time.asctime()
        fobj.write(info)
        fobj.write('\n')
        fobj.close
        print info

    def detectBuild(self):
        breakfn  = "/tmp/nowait"
        sigfn    = self.doneFile
        ret      = True
        info     = 'got signal file from hadoop'
        cmdTimeout = 10
        buildTimeOut = self.config.indexBuildTimeout

        startTime = time.time()

        if os.path.exists(breakfn):
            self.logger.info("INFO: remain ",breakfn, "got removed")
            os.remove(breakfn)

        try:
            while (not self.hadoopWrapper.isPathExists(sigfn,cmdTimeout)):
                time.sleep(5)
                if time.time()  > buildTimeOut + startTime:
                    info = 'Critical - detectBuild timeout !!'
                    self.logger.error(info)
                    self.printLog(info)
                    return False
                
                if os.path.exists(breakfn):
                    info = "Got break files: " + breakfn + " QUIT"
                    ret = False
                    break
        except Exception,e :
            info = str(e)
            ret =  False
        self.logger.info(info)
        return ret

    def getAllClusters(self):
        searchClusters = SearchSystem(self.config)
        searchClusters.GetAllSearchClusters()
        return 

    def updateServiceBegin(self):
        copyfn  = self.copyingFile
        timeout = 10

        if not self.hadoopWrapper.touch(copyfn,timeout):
            info = 'Critical - Touch'  + copyfn + 'Failed Quit!'
            self.logger.error(info)
            sys.exit(1)
        return True

    def updateServiceEnd(self):
        timeout = 10
        self.hadoopWrapper.remove(self.copyingFile,timeout)
        self.hadoopWrapper.remove(self.doneFile,timeout)
        return True
    
    def updateService(self):

        self.updateServiceBegin()

        searchSystem = SearchSystem(self.config)
        errorNo = searchSystem.updateSearchClusters()
        
        if errorNo != error.NO_ERROR:
            info = 'Critical - ' + error.getErrorMessage(errorNo)
            self.logger.error(info)
            self.printLog(info)
            return False
        else:
            info = 'OK - success'
            self.printLog(info)

        self.updateServiceEnd() 
        return True

    def run(self):
        # try:
        if not self.detectBuild():
            return False
        if not self.updateService():  
            return False
        # except Exception, e:
            # info = 'Exception caught: ' + str(e)
            # self.logger.error(info)
            # self.printLog(info)
            # return False
        return True

if __name__ == '__main__':
    controller = Controller()

    def detectBuildOpt(option,opt_str,value,parser):
        controller.detectBuild()

    def switchAggOpt(option,opt_str,value,parser):
        controller.switchAgg()

    def copyHadoopIdxOpt(option,opt_str,value,parser):
        src_fn,dst_fn = value
        controller.copyHadoopIdx(src_fn,dst_fn)

    def listClusterOpt(option,opt_str,value,parser):
        controller.getAllClusters()
 
    def updateServiceOpt(option,opt_str,value,parser):
        controller.updateService()

    def runUpdateWithoutCopy(option,opt_str,value,parser):
        controller.updateServiceWithoutCopy()

    def RunAllOpt(option,opt_str,value,parser):
        controller.updateService()

    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)
    parser.add_option("-d","--detect-build"  ,action="callback",callback=detectBuildOpt)
    parser.add_option("--list-cluster"       ,action="callback",callback=listClusterOpt)
    parser.add_option("--update-service"     ,action="callback",callback=updateServiceOpt)
    parser.add_option("--run-all"     ,action="callback",callback=RunAllOpt)
    (options, args) = parser.parse_args()
