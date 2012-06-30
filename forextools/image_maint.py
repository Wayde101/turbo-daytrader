#!/home/tops/bin/python

import os, sys ,re,string
import configuration
import process


class ImgMaint:
    def __init__(self, config = configuration.Configuration()):
        self.srcpath      = config.mt4shotpath
        self.dstpath      = config.imgbakuppath
        self.rcmd         = config.rsyncbin
        

    def runBakup(self):
        opt = '-avP --exclude \'*.csv\''
        for path in self.srcpath:
            back_cmd = '%s %s %s %s' % (self.rcmd,opt,path,self.dstpath)
            p = process.Process(back_cmd)
            p.runInConsole()

    def runClean(self):

        for path in self.srcpath:
            # clean 1 day ago files
            delcmd = 'find %s -name "*.gif" -ctime +1 -exec rm -f {} \;' % path
            p = process.Process(delcmd)
            p.runInConsole()
        return
        
        

if __name__ == '__main__':

    if 0 != os.getuid():
        print >> sys.stderr, 'become root first!!'
        exit(1)

    b=ImgMaint()
    b.runBakup()
    b.runClean()
    
