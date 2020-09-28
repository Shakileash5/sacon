from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search",methods = ["GET","POST"])
def search():
    if request.method == "POST":
        data = dict(request.form)
        print(data)
    return "200"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)),debug=True,use_reloader=True)