from notification import announcer
from django.conf import settings
import json
from profile.models import Profile
from notification.models import Notification

def send_notification(to,title,message):

	socket = getattr(settings, "NOTIFICATION_WEBSOCKET", None)
	web_socket = announcer.Notification_Client(socket, protocols=['http-only', 'chat'])
	web_socket.connect()
	web_socket.send(
		json.dumps( {
			"stream": "notification",
			"payload": { "to": to, "message":message,"title":title },
			}))
	web_socket.close()

	profile = Profile.objects.get(username=to)
	notification = Notification.objects.create(
		notification_to    = profile,
		title              = "New Order",
		message            = "You Have New Order",
		)
	notification.save()
	return