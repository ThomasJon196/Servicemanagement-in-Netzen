from flask import Flask
from miniwhoami import render_miniwhoami

app = Flask(__name__)

@app.route("/")
def miniwhoami():
    return render_miniwhoami()
