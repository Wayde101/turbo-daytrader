#! /usr/bin/env python

import os, sys ,re
import time
import logging
import log
import configuration
import error

from search_cluster import SearchCluster
from aggregator_wrapper import AggregatorWrapper
from hadoop_tool import HadoopTool

class SearchSystem:
    def __init__(self, config = configuration.Configuration()):
        self.config = config
        self.clusterConfigPaths = config.clusterConfigPaths
        self.logger = logging.getLogger()
        self.swStat = 0   # 0: mean all agg are on service   swStat = 1: Means clusterConfigPaths[swStat -1 ] is on services

        hadoop_client_path = 'hadoop_client/bin'
        hadoopToolPath = os.path.join(os.path.dirname(__file__),hadoop_client_path)
        self.hadoopWrapper = HadoopTool(hadoopToolPath)

    def checkBeforeCopy(self):
        incr_dirs = self.hadoopWrapper.listDirectory(self.config.hadoopIncrRoot)
        if len(incr_dirs) != 0:
            p = re.compile('.*(\d{10}_\d{10})')
            remove_list = []
            for dir in incr_dirs:
                if not p.match(dir):
                    remove_list.append(dir)

            for i in remove_list:
                incr_dirs.remove(i)

            return True, incr_dirs
        return True, incr_dirs
        

    #copy increase data to all SearchCluster and start build job in this service.
    def buildSearchClusters(self):
        (ckIncrRet, ckIncrList) = self.checkBeforeCopy()
        if not ckIncrRet:
            self.logger.info('don\'t find increase data.')
            return error.ERROR_NO_INCR_DATA
        
        self.logger.info(('get increase directory list: [%s]') % (ckIncrList))
        for clusterConfigPath in self.clusterConfigPaths:
            self.logger.info('switch cluster for: [%s]' % clusterConfigPath)

            searchCluster  = SearchCluster(clusterConfigPath, self.config)
            copyRet, copyIncrData   = searchCluster.copyIncrData(ckIncrList)

            if copyRet != error.NO_ERROR:
                self.logger.debug('Copy incr data failed')
                return error.ERROR_BUILD_INCR_INDEX

            self.logger.info(('Copy increase data sucess, the file patern [%s]' % copyIncrData))
            buildIndexRet = searchCluster.buildIncr(copyIncrData)
            if buildIndexRet != error.NO_ERROR:
                self.logger.debug('build increase index failed:[%s]' % clusterConfigPath)
                return buildIndexRet

        if not searchCluster.movePg2Done(ckIncrList):
            self.logger.error('move pangu to done dictionary fail')
            return error.ERROR_INCR_MOVE_PG

        self.logger.debug('begin to move hadoop to done')
        if not searchCluster.moveHdp2Done(ckIncrList):
            self.logger.error('move hadoop to done dictionary fail')
            return error.ERROR_INCR_MOVE_HDP

        return error.NO_ERROR

    #copy index to all SearchCluster and start service in this service.
    def updateSearchClusters(self):
        switchAggregatorTimeout = self.config.switchAggregatorTimeout
        aggregatorWrapper = AggregatorWrapper(self.config)
        
        for clusterConfigPath in self.clusterConfigPaths:
            self.logger.info('switch cluster for: [%s]' % clusterConfigPath)
            # fix switch path info
            # if not aggregatorWrapper.stop(index, switchAggregatorTimeout):    
                # self.logger.debug('switch aggregator failed: [%s]' % clusterConfigPath)
                # return error.ERROR_SWITCH_PROXY_ERROR

            searchCluster  = SearchCluster(clusterConfigPath, self.config)

            if self.config.noCopy == clusterConfigPath or self.config.noCopy == 'all':
                self.logger.info('[%s] running without Copy' % self.config.noCopy )
                copyIndexRet = error.NO_ERROR
            else:
                copyIndexRet   = searchCluster.copyIndex()

            if copyIndexRet   != error.NO_ERROR:
                self.logger.debug('Copy index failed')
                return copyIndexRet

            switchIndexRet = searchCluster.switchIndex()

            if switchIndexRet != error.NO_ERROR:
                self.logger.debug('switch cluster failed:[%s]' % clusterConfigPath)
                return switchIndexRet

        return error.NO_ERROR
        
        # #switch aggregator
        # self.logger.info('recover aggregator...')
        # if not aggregatorWrapper.recover(switchAggregatorTimeout):
            # return error.ERROR_SWITCH_PROXY_ERROR

        # self.logger.info('switch index for clusters completely')
        # return error.NO_ERROR


    def GetAllSearchClusters(self):
        for clusterConfigPath in self.clusterConfigPaths:
            print clusterConfigPath
        return

if __name__ == '__main__':
    searchSystem = SearchSystem()
    status = searchSystem.updateSearchClusters()
    if status != error.NO_ERROR:
        print >> sys.stderr, 'switch index failed: ' + error.getErrorMessage(status)
        sys.exit(1)
    sys.exit(0)
    
    
    
