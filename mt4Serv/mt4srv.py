from twisted.internet import protocol, reactor
from twisted.protocols import basic
import struct
import cjson


class mt4srvProtocol(basic.LineReceiver):
    def dataReceived(self, input_str):
        json_payload = input_str[2:]
        print json_payload
        read_status = self.factory.read_into_bb(json_payload)
        if read_status[0:2] != 'OK':
            print read_status
            self.transport.write(self.factory.mtr(read_status))

        if read_status == 'OKmt4':
            print self.factory.bb
            self.transport.write(self.factory.mtr("in_mt4_proc"))

        if read_status == 'OKconsole':
            print "console proc"

class mt4srvFactory(protocol.ServerFactory):
    protocol = mt4srvProtocol
    def __init__(self, **kwargs):
        self.bb = {'EURUSD_60' : ['null','null'],
                   'EURUSD_5' : ['null','null'],
                   'GBPUSD_60' : ['null','null'],
                   'USDCHF_60' : ['null','null'],
                   'AUDUSD_60' : ['null','null'],
                   'USDCAD_60' : ['null','null'],
                   'USDJPY_60' : ['null','null']
                   }
        
    def read_into_bb(self,jstr):
        jdict=cjson.decode(jstr)
        rt='OKmt4'
        if jdict.has_key('CID'):
            if jdict['CLIENT'] == 'MetaTrader4':
                self.bb[jdict['CID']][0]=jstr
                rt='OKmt4'
            elif jdict['CLIENT'] == 'console':
                self.bb[jdict['CID']][1]=jstr
                rt='OKconsole'
            else:
                rt="NonMt4orConsole"
        else:
            rt="MissSymbolOrClientKey"
        return rt
            
    def mtr(self,string):
        return struct.pack(">H",len(string)) + string

reactor.listenTCP(1984, mt4srvFactory())
reactor.run()

