from flask import Flask
from multiprocessing import Pool
import time

UPLOAD_FOLDER = './Input/Functional_Annotation/'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


import os
import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
from random import randint
import subprocess
#import pipeline_ahish_sonali
ALLOWED_EXTENSIONS = set(['gz'])

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

@app.route('/', methods=['POST'])
def upload_file():
	# check if the post request has the file part
    if ('file1' not in request.files):
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file1 = request.files['file1']
    if (file1.filename == '') :
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if (file1) and (allowed_file(file1.filename)) :
        filename1 = secure_filename(file1.filename)
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
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
        
        #pool = Pool(processes=4)              #start 4 worker processes
        #pool.apply_async(pipeline_ahish_sonali.f, (file1_location,"./sonali_test",file2_location,))   # evaluate "f(10)" asynchronously in a single process
               
        return resp
         
    #else:
       	#resp = jsonify({'message' : 'Allowed format is gzip for FASTA files'})
        #resp.status_code = 400
        #return resp

   
    
    
if __name__ == "__main__":
    app.run()
