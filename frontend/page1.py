from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/genomeassembly")
def genomeassembly():
    return render_template("GenomeAssembly.html")

@app.route("/geneprediction")
def geneprediction():
    return render_template("GenePrediction.html")

@app.route("/func-ann")
def functionalannotation():
    return render_template("FunctionalAnnotation.html")

@app.route("/comp-gen")
def comparativegenomics():
    return render_template("ComparativeGenomics.html")

@app.route("/AboutUs")
def aboutus():
    return render_template("AboutUs.html")

@app.route("/submit")
def submit():
    return render_template("submit.html")


if __name__ == "__main__":
    app.run()
