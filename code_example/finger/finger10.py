# Read username, output from factory interfacing to web, drop connections

from twisted.internet import protocol, reactor, defer, utils
from twisted.protocols import basic
# 引入了 webclient 可以抓取远程的web 并且返回
from twisted.web import client

class FingerProtocol(basic.LineReceiver):
    def lineReceived(self, user):
        d = self.factory.getUser(user)

        def onError(err):
            return 'Internal error in server'
        d.addErrback(onError)

        def writeResponse(message):
            self.transport.write(message + '\r\n')
            self.transport.loseConnection()
        d.addCallback(writeResponse)

class FingerFactory(protocol.ServerFactory):
    protocol = FingerProtocol
    
    def __init__(self, prefix):
        self.prefix=prefix
    
    def getUser(self, user):
        return client.getPage(self.prefix+user)

reactor.listenTCP(1079, FingerFactory(prefix='http://livejournal.com/~'))
reactor.run()
