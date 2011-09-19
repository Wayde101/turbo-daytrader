# Read username, output from factory interfacing to OS, drop connections
# utils 里包含了一些getProcess 一些包装好的工具
from twisted.internet import protocol, reactor, defer, utils
from twisted.protocols import basic

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

    def getUser(self, user):
        return utils.getProcessOutput("finger", [user])

reactor.listenTCP(1079, FingerFactory())
reactor.run()
