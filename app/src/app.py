#!python3
from flask import Flask,request,render_template,redirect
import brawlrec

app = Flask(__name__)
#db_path="scrydb.sqlite"
#cursor = brawlrec.start_db(db_path)


#initialize read only db

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        commanders = brawlrec.getCommanders()
        return render_template("index.html", commanders=commanders)
    elif request.method == 'POST':
        commander = request.form['commander']
        return redirect('/search/'+commander)

@app.route("/search/<cmd>")
def search(cmd):
    results = brawlrec.getMatches(cmd)
    return render_template("search.html", results=results, commander=cmd)

@app.route("/search/<cmd>/paste")
def paste(cmd):
    results = brawlrec.getMatches(cmd)
    return render_template("paste.html", results=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
