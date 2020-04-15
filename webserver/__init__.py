from flask import Flask
from flask_mail import Mail, Message
app = Flask(__name__)
app.config.update(
	DEBUG=True,
	MAIL_SERVER="smtp.gmail.com",
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME='scoliagatech@gmail.com',
	MAIL_PASSWORD='Team3-WebServer'
        )
mail = Mail(app)
from webserver.backend.routes import mod
from webserver.frontend.routes import mod

app.register_blueprint(frontend.routes.mod)
app.register_blueprint(backend.routes.mod,url_prefix='/api')
