#! /usr/bin/env python
import subprocess
import time
import signal
import re
import os
import logging
import log
import pdb

class Process_multiple:
      GlobalTimeout_mult = 0
      intervalSecond_mult = 1
      
      def __init__(self, cmd_list):
          self.cmd_list = cmd_list
          self.logger = logging.getLogger()
          self.cmd_Single = ''
          self.run_p = {}
          self.pnum = 0
      
      def run_multInConsole(self, timeout = GlobalTimeout_mult):
          #pdb.set_trace()
          #tmpOutFile = '.process_run_out%s' % self.pnum
          #tmpErrFile = '.process_run_err%s' % self.pnum
          #self.cmd_Single = self.cmd_Single + ' >' + tmpOutFile + ' 2>' + tmpErrFile
          #self.cmd_Single = '%s > %s 2> %s' % (self.cmd_Single, tmpOutFile, tmpErrFile)
          self.logger.debug(self.cmd_Single)
          self.run_p[self.pnum] = subprocess.Popen(self.cmd_Single, shell=True)
          self.pnum = self.pnum + 1
          time.sleep(2)
      def return_res_list(self):
          return_value={}
          tmp_i = 0
          while tmp_i < self.pnum:
             #tmpOutFile = '.process_run_out' + str(tmp_i)
             #tmpErrFile = '.process_run_err' + str(tmp_i)
             #strout = strerr = ''
             #if os.path.exists(tmpOutFile):
             #    strout = file(tmpOutFile).read()
             #if os.path.exists(tmpErrFile):
             #    strerr = file(tmpErrFile).read()
             self.run_p[tmp_i].wait()
             #return_value[tmp_i]=(self.run_p[tmp_i].returncode, strout, strerr)
             return_value[tmp_i]=(self.run_p[tmp_i].returncode)
             tmp_i = tmp_i + 1
          return return_value
                 
      def run_multresout(self, timeout = GlobalTimeout_mult):
          for self.cmd_Single in self.cmd_list:
              self.run_multInConsole(timeout)
          while timeout > 0:
              time.sleep(self.intervalSecond_mult)
              timeout = timeout - self.intervalSecond_mult
              tmp_i = 0
              sucessful_runed = 0
              while tmp_i < self.pnum:
                  if self.run_p[tmp_i].poll() == None:
                      tmp_i = tmp_i + 1
                  else:
                      if self.run_p[tmp_i].returncode == 0:
                          sucessful_runed = sucessful_runed + 1
                          if sucessful_runed == self.pnum:
                              return_res = self.return_res_list()
                              return return_res
                      else:   
                          self.logger.error("CMD Error: process by id [%s] error_code:[%s]" % ( tmp_i, self.run_p[tmp_i].returncode))
                          return_value={}
                          #tmpOutFile = '.process_run_out' + str(tmp_i)
                          #tmpErrFile = '.process_run_err' + str(tmp_i)
                          #strout = strerr = ''
                          #self.run_p[tmp_i].wait()
                          return_value[0]=(self.run_p[tmp_i].returncode)
                          return return_value
          tmp_i=0
          while tmp_i < self.pnum:
              if self.run_p[tmp_i].poll() == None:
                  os.kill(self.run_p[tmp_i].pid, signal.SIGKILL)
                  self.logger.error("Timout: kill process by id [%s]" % tmp_i)
              tmp_i = tmp_i + 1
          return_res = self.return_res_list()
          return return_res
 
if __name__ == '__main__':
    cmd = ["ping 10.249.128.12", "ping 10.249.128.11"]
    p = Process_multiple(cmd)
    return_res = p.run_multresout(20)
    print return_res
