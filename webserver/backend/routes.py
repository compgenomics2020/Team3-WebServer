from os import path
from flask import Blueprint, Response
#from webserver import create_app
import os
import urllib.request
from flask import Flask, request, redirect, jsonify
from flask import current_app
from werkzeug.utils import secure_filename
from datetime import datetime
from random import randint
from multiprocessing import Pool
import time
import subprocess
from flask_mail import Mail, Message
#from webserver import mail
#print(mail)
from webserver.backend import models 
from webserver.backend import db_util 
from webserver.backend import email_util
pool = Pool(processes=4)
pool3=Pool(processes=4)
from flask import send_file
from webserver.backend import delete_downloads
ALLOWED_EXTENSIONS = set(['gz'])

UPLOAD_FOLDER = './Input/'

BASE_OUTPUT_PATH = './Output/'
#mail=Mail(current_app)
current_app.config.update(
        DEBUG=True,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME='scoliagatech@gmail.com',
        MAIL_PASSWORD='Team3-WebServer'
        )
mail=Mail(current_app)
with current_app.app_context():
	email_util.init_email_sender(mail)

pipeline_dict = {1:'Genome_Assembly', 2:'Gene_Prediction', 3:'Functional_Annotation', 4:'Comparative_Genomics'}
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

##########################################LOOK FROM HERE#############################################

@mod.route('/backend_assembly')
def backend_assembly(new_filename, user_email,pipeline_num,tools,file1_location):
    flag=0
    #MAKE OUTPUT PATH SPECIFIC FOR YOUR TOOL THIS IS JUST A TEST OUTPUT PATH
    output_path=BASE_OUTPUT_PATH+"Genome_Assembly/"+new_filename+".tar.gz"
    #THIS IS JUST AN EXAMPLE FUNCTION
    pool.apply_async(models.f,(10,file1_location,flag,output_path))
    if flag == 0:
    	c1 = db_util.scolia_data(job_id = new_filename, email = user_email ,job_submitted = 0, email_sent = 0, pipeline_number = 3)
    	db_util.insert(c1)
    return(True)

@mod.route('/backend_prediction')
def backend_prediction(new_filename, user_email,pipeline_num,tools,file1_location,file2_location):
    flag=0
    #MAKE OUTPUT PATH SPECIFIC FOR YOUR TOOL THIS IS JUST A TEST OUTPUT PATH
    output_path=BASE_OUTPUT_PATH+"Gene_Prediction/"+new_filename+".tar.gz"
    #THIS IS JUST AN EXAMPLE FUNCTION
    pool.apply_async(models.f,(10,file1_location,flag,output_path))
    if flag == 0:
    	c1 = db_util.scolia_data(job_id = new_filename, email = user_email ,job_submitted = 0, email_sent = 0, pipeline_number = 3)
    	db_util.insert(c1)
    return(True)

@mod.route('/backend_function')
def backend_function(new_filename, user_email,pipeline_num,tools,file1_location):
    print(tools)
    flag=0
    output_path=BASE_OUTPUT_PATH+"Functional_Annotation/"+new_filename+".tar.gz" 
    pool.apply_async(models.f,(10,file1_location,flag,output_path))
    if flag == 0:
    	c1 = db_util.scolia_data(job_id = new_filename, email = user_email ,job_submitted = 0, email_sent = 0, pipeline_number = 3)
    	db_util.insert(c1)
    return(True)

@mod.route('/backend_comparative_with_reference')
def backend_comparative_with_reference(new_filename, user_email,pipeline_num,tools,file1_location,file2_location):
    flag=0
    #MAKE OUTPUT PATH SPECIFIC FOR YOUR TOOL THIS IS JUST A TEST OUTPUT PATH
    output_path=BASE_OUTPUT_PATH+"Comparative_Genomics/"+new_filename+".tar.gz"
    #THIS IS JUST AN EXAMPLE FUNCTION
    pool.apply_async(models.f,(10,file1_location,flag,output_path))
    if flag == 0:
    	c1 = db_util.scolia_data(job_id = new_filename, email = user_email ,job_submitted = 0, email_sent = 0, pipeline_number = 3)
    	db_util.insert(c1)
    return(True)

@mod.route('/backend_comparative_no_reference')
def backend_comparative_no_reference(new_filename, user_email,pipeline_num,tools,file1_location):
    flag=0
    #MAKE OUTPUT PATH SPECIFIC FOR YOUR TOOL THIS IS JUST A TEST OUTPUT PATH
    output_path=BASE_OUTPUT_PATH+"Comparative_Genomics/"+new_filename+".tar.gz"
    #THIS IS JUST AN EXAMPLE FUNCTION
    pool.apply_async(models.f,(10,file1_location,flag,output_path))
    if flag == 0:
    	c1 = db_util.scolia_data(job_id = new_filename, email = user_email ,job_submitted = 0, email_sent = 0, pipeline_number = 3)
    	db_util.insert(c1)
    return(True)

##########################################TO HERE FOR YOUR FUNCTION#######################################

@mod.route('/backend_setup')
def backend_setup(files,user_email,pipeline_num,tools):
    UPLOAD_FOLDER = './Input/'
    new_filename = generate_job_id()
    print(user_email)
    flag=0

##################SETS UP FUNCTIONS WITH TWO FILE INPUTS##############################
    if len(files)>1:
    	file1=files[0]
    	file2=files[1]
    	if (file2.filename == '') or (file1.filename=='') :
    		resp = jsonify({'message' : 'No file selected for uploading'})
    		resp.status_code = 400
    		return resp
    	if (file1 and file2) and (allowed_file(file1.filename)) :
    		filename1 = secure_filename(file1.filename)
    		UPLOAD_FOLDER=UPLOAD_FOLDER+pipeline_dict.get(pipeline_num)+"/"
    		file1.save(os.path.join(UPLOAD_FOLDER, filename1))
    		filename2=secure_filename(file2.filename)
    		file2.save(os.path.join(UPLOAD_FOLDER, filename2))
    		resp = jsonify({'message' : 'File successfully uploaded'})
    		resp.status_code = 201
    		
    		subprocess.run("mkdir "+UPLOAD_FOLDER+new_filename, shell = True)
    		subprocess.run("mv "+UPLOAD_FOLDER+file1.filename+" "+UPLOAD_FOLDER+new_filename+"/", shell = True)
    		subprocess.run("mv "+UPLOAD_FOLDER+file2.filename+" "+UPLOAD_FOLDER+new_filename+"/", shell = True)
    		file1_location=UPLOAD_FOLDER+new_filename+"/"+file1.filename.rsplit('.')[0]
    		file2_location=UPLOAD_FOLDER+new_filename+"/"+file2.filename
    		subprocess.run("tar -C "+UPLOAD_FOLDER+new_filename +"/ -zxvf "+UPLOAD_FOLDER+new_filename+"/"+file1.filename, shell = True)
    		subprocess.run("rm "+UPLOAD_FOLDER+new_filename+"/"+file1.filename, shell = True)
    	if pipeline_num==2:
    		result=backend_prediction(new_filename,user_email,pipeline_num,tools,file1_location,file2_location)
    		return(result)
    	if pipeline_num==4:
    		result=backend_comparative_with_reference(new_filename,user_email,pipeline_num,tools,file1_location,file2_location)
    		return(result)

##########SETS UP FUNCTIONS WITH ONLY 1 FILE INPUT######################### 	            
    elif len(files)<=1:
    	file1=files[0]
    	if (file1.filename == ''):
    		resp= jsonify({'message' : 'No file selected for uploading'})
    		resp.status_code = 400
    		return resp
    	if (file1) and (allowed_file(file1.filename)):
    		filename1=secure_filename(file1.filename)
    		UPLOAD_FOLDER=UPLOAD_FOLDER+pipeline_dict.get(pipeline_num)+"/"
    		file1.save(os.path.join(UPLOAD_FOLDER,filename1))
    		subprocess.run("mkdir "+UPLOAD_FOLDER+new_filename, shell = True)
    		subprocess.run("mv "+UPLOAD_FOLDER+file1.filename+" "+UPLOAD_FOLDER+new_filename+"/", shell = True)
    		file1_location=UPLOAD_FOLDER+new_filename+"/"+file1.filename.rsplit('.')[0]
    		subprocess.run("tar -C "+UPLOAD_FOLDER+new_filename +"/ -zxvf "+UPLOAD_FOLDER+new_filename+"/"+file1.filename, shell = True)
    		subprocess.run("rm "+UPLOAD_FOLDER+new_filename+"/"+file1.filename, shell = True)

    		if pipeline_num==3:
    			result=backend_function(new_filename,user_email,pipeline_num,tools,file1_location)
    			return(result)
    		if pipeline_num==1:
    			result=backend_assembly(new_filename,user_email,pipeline_num,tools,file1_location)
    			return(result)
    		if pipeline_num==4:
    			result=backend_comparative_no_reference(new_filename,user_email,pipeline_num,tools,file1_location)
    			return(result)
	
    	else:
    		resp = jsonify({'message' : 'Allowed format is gzip for FASTA files'})
    		resp.status_code = 400
    		return resp

@mod.route("/download", methods=['GET'])
def download_processed_files():
    job_id = str(request.args.get("id"))
    row = db_util.get_one(job_id)
    pipeline_number = row.pipeline_number
    file_path = "."+BASE_OUTPUT_PATH+pipeline_dict.get(pipeline_number)+"/"+job_id+".tar.gz"
    file_path_delete=BASE_OUTPUT_PATH+pipeline_dict.get(pipeline_number)+"/"+job_id+".tar.gz"
    pool3.apply_async(delete_downloads.f,(file_path_delete,int(job_id),))
    if path.exists(file_path_delete):
    	return send_file(file_path, as_attachment=True)
    else:
    	return 'file session expired'	
