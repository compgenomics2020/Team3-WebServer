from flask import Flask, redirect, url_for, render_template,Blueprint,request
from flask_mail import Mail, Message,current_app

mod=Blueprint('frontend',__name__,template_folder='templates',static_folder='static',static_url_path='/frontend/static')
from webserver import mail

app = Flask(__name__)


@mod.route("/")
def homepage():
    return render_template("index.html")

@mod.route("/genomeassembly")
def genomeassembly():
    return render_template("GenomeAssembly.html")

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

