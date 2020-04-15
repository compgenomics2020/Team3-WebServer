from flask import Blueprint

#from api.models import Process_File

mod=Blueprint('backend',__name__)

@mod.route('/getStuff',methods=['GET', 'POST'])
def getStuff(path,filename):
	if request.method == 'POST':
		return '{"result" : "You are in the API!!!}'

