#!python3
from flask import Flask,request,render_template,redirect
import brawlrec

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        commander = request.form['commander']
        return redirect('/search/'+commander)

@app.route("/search/<cmd>")
def search(cmd):
    results = brawlrec.getMatches(cmd)
    return render_template("search.html", results=results)