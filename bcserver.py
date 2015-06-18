import six;
from txws import WebSocketFactory;
from twisted.internet import protocol, reactor;
from bareconductive import BareConductive;
import json;

class VS(protocol.Protocol):


	def connectionMade(self):
		"""
		Callback executed when the client successfully connects to the server.
		"""
		print "CONNECTED"
		
		# Notify the client that a connection has been established

		self.transport.write('server.connected()')
		self.bc=BareConductive();
		self.bc.open();

	def dataReceived(self, req):

		"""
		:param req: Python instruction sent by the client
		:type req: str
		
		Evaluates the instruction `req` sent by the client and responds with an identical instruction, in which the return value of that instruction is the input argument.
		"""
			
		commands=req.split(" ");
		if commands[0]=="read":
			amount=1;
			if len(commands)>1:
				amount=int(commands[1]);
				for i in range(amount):
					self.transport.write(json.dumps(self.bc.read()));
			else:
				while 1:
					self.transport.write(json.dumps(self.bc.read()));



	def connectionLost(self, reason):
			"""
			Callback executed when the connection to the client is lost.
			"""
			print "OOPS, DISCONNECTED";
			self.bc.close();


class VSFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return VS()

if __name__=='__main__':
	try:
		ip_addr, port = "127.0.0.1", 9099

		device = None
		
		print "LISTENING AT %s:%s"%(ip_addr, port)
		
		connector = reactor.listenTCP(port, WebSocketFactory(VSFactory()))
		reactor.run()

	except Exception as e:
		print traceback.format_exc()
