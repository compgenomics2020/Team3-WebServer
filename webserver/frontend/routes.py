from flask import Flask, redirect, url_for, render_template,Blueprint,request, jsonify
from flask_mail import Mail, Message,current_app

mod=Blueprint('frontend',__name__,template_folder='templates',static_folder='static',static_url_path='/frontend/static')
from webserver import mail
from webserver.backend import routes as backend_mod
app = Flask(__name__)


@mod.route("/")
def homepage():
    return render_template("index.html")

@mod.route("/genomeassembly")
def genomeassembly():
    return render_template("GenomeAssembly.html")

@mod.route("/send_message",methods=['POST'])
def send_message():
	email_usr=request.form.get('assem_email')
	directory="../downloads"
	did_send=backend_mod.send_message_back(email_usr,directory)
	if did_send:
		confirm_msg='Your message has been sent!'
		return render_template("submit.html",confirm_msg=confirm_msg)

@mod.route("/geneprediction")
def geneprediction():
    return render_template("GenePrediction.html")

@mod.route("/func-ann")
def functionalannotation():
    return render_template("FunctionalAnnotation.html")

@mod.route("/comp-gen")
def comparativegenomics():
    return render_template("ComparativeGenomics.html")

@mod.route("/AboutUs")
def aboutus():
    return render_template("AboutUs.html")

@mod.route("/submit")
def submit():
    return render_template("submit.html")

@mod.route('/Functional_Annotation',methods=['POST'])
def Functional_Annotation():

	email=request.form.get("ann_email")

	# check if the post request has the file part
	if ('file1' not in request.files):
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file1 = request.files['file1']
	did_send=backend_mod.backend_functional(file1,email)
	if did_send:
		confirm_msg='File Submitted!'
		return render_template("submit.html",confirm_msg=confirm_msg)
	
