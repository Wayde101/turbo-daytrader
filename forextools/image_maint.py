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
        delcmd = 'find . -name "*.gif" -ctime +1 -exec rm -f {} \;'
        for path in self.srcpath:
            findcmd = '%s' % (delcmd)
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
    
