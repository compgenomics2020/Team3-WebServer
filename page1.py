from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/genomeassembly")
def genomeassembly():
    return render_template("GenomeAssembly.html")

@app.route("/functional")
def functionalanotation():
    return render_template("FunctionalAnnotation.html")

if __name__ == "__main__":
    app.run()
