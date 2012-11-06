#! /usr/bin/env python

import os, sys, time, re
import logging
import log
import process

class PanguWrapper:
    def __init__(self, excutable = None):
        if excutable != None:
            self.excutable = excutable
        else:
            self.excutable = 'pu'
        self.logger = logging.getLogger()

    def getPanguFileContent(self, filePath, timeout = 0):
        tmpFileName = 'tmp_file' + str(time.time())
        cmd = self.excutable + ' cp ' + filePath + ' ' + tmpFileName
        p = process.Process(cmd)
        retcode, stdout, stderr = p.run(timeout)
        if retcode != 0 :
            self.logger.error('pangu cp active file [%s] error' % filePath)
            os.remove(tmpFileName)
            return None

        #pattern = re.compile('file\s+copied\s\(downloaded\s\d+bytes\)\.')
        f = open(tmpFileName)
        content = f.read()
        os.remove(tmpFileName)
        return content

    def listPanguDirectory(self, dirPath, timeout = 0):
        cmd = self.excutable + ' ls ' + dirPath
        p = process.Process(cmd)
        retcode, stdout, stderr = p.runWithoutPipe(timeout)
        if retcode != 0 :
            self.logger.error('pu ls directory [%s] error' % dirPath)
            return None
        retItems = []
        for item in re.split('\s+', stdout):
            #item = item.rstrip("/")
            if len(item) != 0:
                retItems.append(item)
        return retItems

    def removeDir(self, dirPath, timeout = 0):
        cmd = 'echo y | ' + self.excutable + ' rmdir ' + dirPath
        p = process.Process(cmd)
        retcode, stdout, stderr = p.runWithoutPipe(timeout)
        if retcode != 0 :
            self.logger.error('pu remove directory [%s] error' % dirPath)
            return False
        return True        

    def removeFile(self, filePath, timeout = 0):
        cmd = 'echo y | ' + self.excutable + ' rm ' + filePath
        p = process.Process(cmd)
        retcode, stdout, stderr = p.runWithoutPipe(timeout)
        if retcode != 0 :
            self.logger.error('pu remove directory [%s] error' % filePath)
            return False
        return True        

    def makeDir(self, dirPath, timeout=0):
        cmd = self.excutable + ' mkdir ' + dirPath
        p = process.Process(cmd)
        retcode, stdout, stderr = p.runWithoutPipe(timeout)
        if retcode != 0 :
            self.logger.error('pu mkdir directory [%s] error' % dirPath)
            return False
        return True        

    def mvDir(self, srcPath, dstPath, timeout=0):
        cmd = self.excutable + ' mvdir ' + srcPath + ' ' + dstPath
        p = process.Process(cmd)
        retcode, stdout, stderr = p.runWithoutPipe(timeout)
        if retcode != 0 :
            self.logger.error('pu mv directory [%s] to [%s] error' , srcPath, dstPath)
            return False
        return True        

def printUsage():
    print >> sys.stderr, sys.argv[0] + ' cat filePath'
    print >> sys.stderr, sys.argv[0] + ' ls dirPath'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        printUsage()
        sys.exit(1)

    panguWrapper = PanguWrapper()
    command = sys.argv[1]
    if command == 'cat':
        content = panguWrapper.getPanguFileContent(sys.argv[2])
        print content
    elif command == 'ls':
        subItems = panguWrapper.listPanguDirectory(sys.argv[2])
        print subItems
    else:
        print >> sys.stderr, 'unsupport command'
        printUsage()
        sys.exit(1)
