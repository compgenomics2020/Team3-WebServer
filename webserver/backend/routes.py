from flask import Blueprint Response

#from api.models import Process_File

mod=Blueprint('backend',__name__)

@mod.route('/send_message_backend')
def send_message_back(email,filename):
	msg=Message(
		subject='Scolia output',
		sender='scoliagatech@gmail.com',
		reciepients=
			[email])
	with mod.open_resource("../downloads/test.txt") as fp:
		msg.attach("test.txt",test/txt",fp.read())
	mail.send(msg)
	confirm_msg = 'Your message has been sent!"
	return (True)
@mod.route("/download_display")
def download_display():
	return'''
	<html><body>
	Hello. <a href="/backend/get_Output">Click me.</a>
	</body></html>
	'''
@mod.route('/get_Output'):
def get_Output():
	with mod.open_resource("../downloads/test.txt") as fp:
                test=fp.read()
	return Response(
		test,
		mimetype="text/plain",
		headers={"Content-disposition":
			"attachment; filename=my_test.txt"})

