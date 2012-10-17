#! /usr/bin/env python

import os, sys ,re
import time
import logging
import log
import configuration
import error

from runtime_service import RuntimeService
from build_service import BuildService
from pangu_wrapper import PanguWrapper
from hdfs2pangu import Hdfs2Pangu
from yishan_hadoop import YishanConfig
from cluster_warmer import ClusterWarmer
from hadoop_tool import HadoopTool

class SearchCluster:
    def __init__(self, configRootPath, config = configuration.Configuration()):
        self.configRootPath = configRootPath
        print "XXX", configRootPath
        self.yishanConf   = YishanConfig(configRootPath)
        self.h2p          = Hdfs2Pangu(configRootPath)
        self.puCon        = PanguWrapper()
        self.nvwaAddr     = self.yishanConf.destnuwa
        self.configuration = config
        self.panguPort    = '10240'
        self.idxPathRoot  = 'pangu://' + self.nvwaAddr + ':' + self.panguPort + self.configuration.panguDataRoot 

        self.services = self.configuration.services
        self.ha2ToolPath = self.configuration.ha2ToolPath
        self.comboMap = self.configuration.comboMap

        hadoop_client_path = 'hadoop_client/bin'
        hadoopToolPath = os.path.join(os.path.dirname(__file__),hadoop_client_path)

        self.runtimeServices = []
        self.buildServices = []

        self.hdpIncrSrc     = config.hadoopIncrRoot
        self.pgIncrDest4YG  = config.panguIncrRoot
        self.hdpDoneDir = os.path.join(self.hdpIncrSrc,'done')
        self.pgDoneDir  = 'pangu://' + self.nvwaAddr + ':' + self.panguPort + os.path.join(self.pgIncrDest4YG,'done/')
        self.pgIncrDest = 'pangu://' + self.nvwaAddr + ':' + self.panguPort + self.pgIncrDest4YG
        self.hadoopWrapper = HadoopTool(hadoopToolPath)

        for serviceName in self.services.keys():
            configPath = configRootPath + '/' + serviceName + '_config'
            self.runtimeServices.append(RuntimeService(self.idxPathRoot,configPath,config,serviceName))

            for clusterName in self.configuration.services[serviceName]:
                self.buildServices.append(BuildService(self.idxPathRoot, configPath, config, serviceName, clusterName))

        self.logger = logging.getLogger()

        
    def getDirName(self, dir):
        p = re.compile('.*(\d{10}_\d{10})')
        if p.match(dir):
            dir_patern = p.search(dir).groups(1)[0]
            return True, dir_patern
        else:
            return False, ''

    def moveHdp2Done(self, dirs):
        self.logger.info("begin to move hadoop to done directory")

        if not self.hadoopWrapper.isPathExists(self.hdpDoneDir):
            print 'hdpDoneDir [%s] does not exists, create it' % self.hdpDoneDir
            self.hadoopWrapper.mkdir(self.hdpDoneDir)

        for dir in dirs:
            getDirNameRet, dirName = self.getDirName(dir)
            path = os.path.join(self.hdpIncrSrc + dirName)
            self.logger.debug(("move hadoop to done, [%s] => [%s]") % (path, self.hdpDoneDir))
            mv_ret = self.hadoopWrapper.move(path, self.hdpDoneDir)
            if not mv_ret:
                self.logger.error(("move hadoop to done dictionary faild. from [%s] to [%s]") % (dir, self.hdpDoneDir))
                return False

        return True

    def movePg2Done(self, dirs):
        self.logger.info("begin to move pangu to done dictionary")

        if self.puCon.listPanguDirectory(self.pgDoneDir) == None:
            print 'pgDoneDir [%s] does not exists,created it' % self.pgDoneDir
            self.puCon.makeDir(self.pgDoneDir)

        for dir in dirs:
            getDirNameRet, dirName = self.getDirName(dir)
            path = self.pgIncrDest + dirName
            dest = self.pgDoneDir + dirName
            self.logger.debug(("move pangu to done, [%s] => [%s]") % (path, self.pgDoneDir))
            mv_ret = self.puCon.mvDir(path, dest)
            if not mv_ret:
                self.logger.error(("move pangu to done dictionary faild. from [%s] to [%s]") % (path, self.pgDoneDir))
                return False

        return True

    def h2pCopy(self, src, dest, timeout = 0):
        if not self.h2p.copyData(src, dest, timeout):
            return False

        dest2 = ''
        if dest[-1] == '/':
            dest2 = dest
        else:
            dest2 = dest + '/'

        if self.puCon.listPanguDirectory('pangu://' + self.nvwaAddr + ':' + self.panguPort + dest2) == None:
            return False
        return True

    def copyIncrData(self, ckIncrList):
        timeout = 1200

        copied_paterns = []
        for dir_name in ckIncrList:
            info="Incr Copy OK!"
            getNameRet, dir_patern = self.getDirName(dir_name)
            if not getNameRet:
                continue

            for loop in range(3):
                self.logger.info(("copy increase data. try [%d]") % loop)

                copy_dest = os.path.join(self.pgIncrDest4YG,dir_patern)
                self.puCon.removeDir(copy_dest)
                if self.h2pCopy(dir_name, copy_dest,timeout):
                    break

            if loop > 3:
                #copy fail
                self.logger.error(("copy increase data fail. from [%s] to [%s]") % (dir_name, os.path.join(self.pgIncrDest4YG,dir_patern)))
                return error.ERROR_COPY_INCR_DATA, copied_paterns
            
            self.logger.info(("copy increase data success. from [%s] to [%s]") % (dir_name, os.path.join(self.pgIncrDest4YG,dir_patern)))
            copied_dir = os.path.join(self.pgIncrDest4YG,dir_patern)
            copied_paterns.append(copied_dir)

            for key in self.configuration.comboMap.keys():
                dump_dir='dump_' + self.configuration.comboMap[key]
                lst_res = self.puCon.listPanguDirectory(self.pgIncrDest + dir_patern + '/' + dump_dir + '/')
                if lst_res == None:
                    continue
                if len(lst_res) <= 0:
                    self.logger.info(("the cluster increase directory is empty. [%s]") % (self.pgIncrDest + dir_patern + '/' + dump_dir + '/'))
                    self.puCon.removeDir(self.pgIncrDest + dir_patern + '/' + dump_dir + '/')
                    continue
                
                for fn in lst_res:
                    if fn.find('/') != -1:
                        self.puCon.removeDir(self.pgIncrDest + dir_patern + '/' + dump_dir + '/' + fn )
                    if fn.find('part-m') == -1:
                        self.puCon.removeFile(self.pgIncrDest + dir_patern + '/' + dump_dir + '/' + fn )

        return error.NO_ERROR, copied_paterns


    def buildIncr(self, incr_data):
        if(len(incr_data) == 0):
            self.logger.info("No Data for build")
            return error.ERROR_NO_INCR_DATA

        for buildService in self.buildServices:
            buildService.setNoData(False)
            pathlist = []
            for path in incr_data:
                pgPath = 'pangu://' + self.nvwaAddr + ':' + self.panguPort + path
                self.logger.debug(('path [%s]') % (path))
                self.logger.debug(('path join [%s] + [%s] => [%s]') % (pgPath, self.comboMap[buildService.clusterName],os.path.join(pgPath, 'dump_' + self.comboMap[buildService.clusterName])))
                tmppath = os.path.join(pgPath, 'dump_' + self.comboMap[buildService.clusterName] + '/')
                self.logger.debug(('tmppath: [%s]') % (tmppath))
                lst_tmp = self.puCon.listPanguDirectory(tmppath)
                if lst_tmp != None and len(lst_tmp) > 0:
                    pathlist.append(tmppath)

            self.logger.info(('start build [%s] increase') % buildService.clusterName)
            self.logger.info(('the file patern list:[%s]') % pathlist)
            if (len(pathlist) == 0):
                self.logger.info(('file patern list is null, clusterName:[%s]') % buildService.clusterName)
                buildService.setNoData(True)
                continue

            if buildService.buildIncrIndex(pathlist, 300) != error.NO_ERROR:
                return error.ERROR_BUILD_INCR_INDEX

        for buildService in self.buildServices:
            if buildService.waitBuildIncrIndex(3600) != error.NO_ERROR:
                return error.ERROR_BUILD_INCR_INDEX
            
        return error.NO_ERROR

    def copyIndex(self):
        self.logger.info('Copy Begining ...')

        for service, clusters in self.configuration.services.items():
            print "clusters is:", self.configuration.services[service]

        hdp_dat_dir = self.configuration.hadoopDumpRoot
        pg_tmp_dir  = self.configuration.panguDataRoot + 'tmpdata'

        retry_time = self.configuration.idxCopyRetryTimes
        while retry_time > 0:
            if self.puCon.listPanguDirectory(self.idxPathRoot + 'tmpdata/' ) != None:
                self.puCon.removeDir(self.idxPathRoot + 'tmpdata/')

            h2pCopy = self.h2p.copyData(hdp_dat_dir,pg_tmp_dir)
            if h2pCopy:
                break;
            retry_time-=1
            self.logger.info("Copy failed from [%s] to [%s], last retry [%d]" , hdp_dat_dir, pg_tmp_dir, retry_time)
            if retry_time <= 0:
                self.logger.error("Copy failed from [%s] to [%s]" , hdp_dat_dir, pg_tmp_dir)
                return error.ERROR_COPY_INDEX

        for rs in self.runtimeServices:
            for cluster in self.configuration.services[rs.serviceName]:
                serv_src_path    = self.idxPathRoot + 'tmpdata/' + self.configuration.comboMap[cluster][0]
                serv_dest_path   = self.idxPathRoot  + \
                    rs.serviceName + '/runtimedata/' + cluster + '/' + cluster 

                max_gen_ver = self.checkRuntimedataDir(serv_dest_path)
                next_ver = max_gen_ver + 1
                serv_dest_path   = serv_dest_path + '/generation_%d' % next_ver
                self.logger.info("from [%s] to [%s]. Begining" , serv_src_path, serv_dest_path)
                # move index data from tmpdata
                if not self.puCon.mvDir(serv_src_path,serv_dest_path):
                    self.logger.error("Move failed from [%s] to [%s]" , serv_src_path, serv_dest_path)
                    return error.ERROR_COPY_INDEX
                
            self.logger.info('copy index for [%s] done ' % rs.serviceName)

        return error.NO_ERROR

    def checkRuntimedataDir(self,destDir):
        max_ver   = 0
        all_ver   = []
        dst_dir   = destDir
        p=re.compile('generation_([0-9]*)')

        if self.puCon.listPanguDirectory(dst_dir) == None:
            self.puCon.makeDir(dst_dir)
            return max_ver

        for line in self.puCon.listPanguDirectory(dst_dir):
            if p.match(line):
                pat_num = p.search(line).groups(1)[0]
                all_ver.append(int(pat_num))

        if len(all_ver) != 0:
            max_ver = max(all_ver)
        
        return max_ver

    def checkConfigurationDir(self,destDir):
        timeout = 10
        if self.puCon.listPanguDirectory(destDir, timeout) == None:
            self.puCon.makeDir(destDir,timeout)
        return True
        

    def switchIndex(self):
        self.logger.info('switch index for [%s]' % self.configRootPath)
        self.logger.info('get old serving config and index version...')
        
        
        # for rs in self.runtimeServices:
            # self.logger.info('switching index for [%s]' % rs.serviceName)
        

        #stop all Service
        if not self.stopAllService():
            return error.ERROR_STOP_SERVICE

        # deploy configuration
        if not self.deployConfiguration():
            return error.ERROR_DEPLOY_CONFIGURATION

        #start service
        ret = self.startAllService()
        return ret

    def stopAllService(self):
        for runtimeService in self.runtimeServices:
            if not runtimeService.stopService():
                self.logger.error('stop all service error: [%s]' % self.configRootPath)
                return False
        return True

    def startAllService(self):
        for runtimeService in self.runtimeServices:
            status = runtimeService.startService()
            if  status != error.NO_ERROR:
                return status
        if not self.warmupAllService():
            return error.ERROR_LOAD_PARTITION_FAILED
        if not self.checkAllService():
            return error.ERROR_LOAD_PARTITION_FAILED
        return error.NO_ERROR


    def warmupAllService(self):
        clusterWarmer = ClusterWarmer(self.configRootPath,self.configuration)
        threadNum = self.configuration.abenchThreadNum
        timeLen = self.configuration.abenchTimeLen
        if not clusterWarmer.startAbench(threadNum, timeLen):
            return False
        return True



    def deployConfiguration(self):
        self.logger.info('delployConfigurations begining')
        for rs in self.runtimeServices:
            if not rs.deployConfiguration():
                self.logger.error('deploy configuration error: [%s]' % rs.serviceName)
                return False
        return True

    def serviceCheckup(self):
        self.logger.info('service Checking up')
        for rs in self.runtimeServices:
            if not rs.getServiceStatusOk():
                rs.serviceStart()
                self.logger.error('deploy configuration error: [%s]' % rs.serviceName)
                return False

    def switchIndexing(self):
        self.logger.info('switch index begining')
        for rs in self.runtimeServices:
            if not rs.switchIndexing():
                self.logger.error('switch index error: [%s]' % rs.serviceName)
                return False
        return True

    def checkAllService(self):
        self.logger.info('checking AllService: [%s]')
        for runtimeService in self.runtimeServices:
            if not runtimeService.checkStartCorrect():
                return False
        return True


    def warmupAllService(self):
        clusterWarmer = ClusterWarmer(self.configRootPath)
        threadNum = self.configuration.abenchThreadNum
        timeLen = self.configuration.abenchTimeLen
        if not clusterWarmer.startAbench(threadNum, timeLen):
            return False
        return True

if __name__ == '__main__':
    searchCluster = SearchCluster("/apsarapangu/disk5/daogou/crontab/pe_code/index_switcher/ay33_kuafu2")

    print searchCluster.checkRuntimedataDir('pangu://localcluster/home/admin/daogou/daogou_combo/runtimedata/daogou_luntan/daogou_luntan')
