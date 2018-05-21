from ws4py.websocket import WebSocket
from ws4py.client.threadedclient import WebSocketClient
import json

class Notification_Client(WebSocketClient):

	def closed(self, code, reason=None):
		print "Closed down", code, reason

	def received_message(self, m):
		print m
		if len(m) == 175:
			self.close(reason='Bye bye')






        