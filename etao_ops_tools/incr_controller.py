#! /usr/bin/env python
import os, sys, re, time
import pickle
import logging
import configuration
import util
import error

from optparse import OptionParser
from search_system import SearchSystem

class IncrController:
    def __init__(self, configuration = configuration.Configuration()):
        self.config = configuration
        hadoop_client_path = 'hadoop_client/bin'
        self.doneFile =  configuration.doneFile
        self.copyingFile =configuration.copyingFile

        hadoopToolPath = os.path.join(os.path.dirname(__file__),hadoop_client_path)

        self.incr_dirs  = []
        self.pangu_incr_dirs = []
        self.copied_paterns = []

        self.searchSystem=SearchSystem(self.config)

        self.logger = logging.getLogger()


    def printLog(self, info):
        fobj = open(self.eagleLogFile, 'a')
        info = info + ' ' + time.asctime()
        fobj.write(info)
        fobj.write('\n')
        fobj.close
    def run(self):
        self.logger.info('instrease build will start')

        build_cluster = self.searchSystem.buildSearchClusters()
        if build_cluster != error.NO_ERROR and build_cluster != error.ERROR_NO_INCR_DATA:
            # self.printLog('Critical: build Increase data failed')
            self.logger.error('Critical: build Increase data failed')
            return False

        self.logger.info('build Increase completed')
        return True

if __name__ == '__main__':
    controller = IncrController()

    def RunAllOpt(option,opt_str,value,parser):
        controller.run()

    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage)

    parser.add_option("--run-all"     ,action="callback",callback=RunAllOpt)
    (options, args) = parser.parse_args()
