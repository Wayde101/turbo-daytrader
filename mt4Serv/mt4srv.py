from twisted.internet import protocol, reactor
from twisted.protocols import basic

class mt4srvProtocol(basic.LineReceiver):
    def lineReceived(self, mt4in):
#        self.transport.write(self.factory.getUser(user)+"\r\n")
        print mt4in

class mt4srvFactory(protocol.ServerFactory):
    protocol = mt4srvProtocol
    def __init__(self, **kwargs):
        print kwargs
        self.users = kwargs

    def getUser(self, user):
        return self.users.get(user, "No such user")

reactor.listenTCP(1984, mt4srvFactory(moshez='Happy and well'))
reactor.run()

