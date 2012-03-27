# Read username, output from empty factory, drop connections

from twisted.internet import protocol, reactor
from twisted.protocols import basic

class FingerProtocol(basic.LineReceiver):
    #只处理收发，逻辑交给factory 
    def lineReceived(self, user):
        self.transport.write(self.factory.getUser(user)+"\r\n")
        self.transport.loseConnection()

class FingerFactory(protocol.ServerFactory):
    protocol = FingerProtocol

    # getUser logic moved to Factory
    def getUser(self, user):
        return "No such user"

reactor.listenTCP(1079, FingerFactory())
reactor.run()
