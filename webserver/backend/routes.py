from flask import Blueprint, Response
#from webserver import create_app
import os
import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from random import randint
from multiprocessing import Pool
import time
import subprocess
from webserver import mail
from webserver.backend import models 
from webserver.backend import db_util 
from webserver.backend import email_util
pool = Pool(processes=4)

ALLOWED_EXTENSIONS = set(['gz'])
UPLOAD_FOLDER = './Input/Functional_Annotation/'

#with app.app_context():
#pool2 = Pool(processes=4)
#pool2.apply_async(email_util.init_email_sender,(mail,))

mod=Blueprint('backend',__name__)

def allowed_file(filename):
    #print(filename.rsplit('.', 1)[1].lower())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
"""
def allowed_format(filename):
        return
"""
def generate_job_id():
    r1 = randint(0,9)
    r3 = randint(0,9)
    r2=datetime.today().strftime('%Y%m%d%H%M%S')
    return (str(r1)+r2+str(r3))
	
@mod.route('/send_message_backend')
def send_message_back(email,filename):
	msg=Message(
		subject='Scolia output',
		sender='scoliagatech@gmail.com',
		reciepients=
			[email])
	with mod.open_resource("../downloads/test.txt") as fp:
		msg.attach("test.txt","test/txt",fp.read())
	mail.send(msg)
	confirm_msg = 'Your message has been sent!'
	return (True)
@mod.route("/download_display")
def download_display():
	return'''
	<html><body>
	Hello. <a href="/backend/get_Output">Click me.</a>
	</body></html>
	'''
@mod.route('/get_Output')
def get_Output():
	with mod.open_resource("../downloads/test.txt") as fp:
                test=fp.read()
	return Response(
		test,
		mimetype="text/plain",
		headers={"Content-disposition":
			"attachment; filename=my_test.txt"})

@mod.route('/backend_functional')
def backend_functional(file1,user_email):
    flag=0
	# check if the post request has the file part
    if (file1.filename == '') :
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if (file1) and (allowed_file(file1.filename)) :
        filename1 = secure_filename(file1.filename)
        file1.save(os.path.join(UPLOAD_FOLDER, filename1))
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
         

        new_filename = generate_job_id()
            
        ###Moving files to job ID folder####
        subprocess.run("mkdir ./Input/Functional_Annotation/"+new_filename, shell = True)
        subprocess.run("mv ./Input/Functional_Annotation/"+file1.filename+" ./Input/Functional_Annotation/" +new_filename+"/", shell = True)
        #print(file2.filename)
            
        #######Unzipping the gz folder######
        subprocess.run("tar -C ./Input/Functional_Annotation/"+new_filename +"/ -zxvf ./Input/Functional_Annotation/"+new_filename+"/"+file1.filename, shell = True)
        subprocess.run("rm "+"./Input/Functional_Annotation/"+new_filename+"/"+file1.filename, shell = True)

       ###########async call############
        
        file1_location = "./Input/Functional_Annotation/"+new_filename+"/"+file1.filename.rsplit('.')[0]
        #file2_location = "./Input/Gene_Prediction/"+new_filename+"/"+file2.filename
       
        print(file1_location)
        
        pool.apply_async(models.f,(10,file1_location,flag,))   # evaluate "f(10)" asynchronously in a single process
	
        if flag == 0:
            c1 = db_util.scolia_data(job_id = new_filename, email = user_email ,job_submitted = 0, email_sent = 0, pipeline_number = 3)
            db_util.insert(c1)

        return (True)
         
    else:
       	resp = jsonify({'message' : 'Allowed format is gzip for FASTA files'})
        resp.status_code = 400
        return resp
