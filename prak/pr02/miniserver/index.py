from flask import Flask
from miniwhoami import render_miniwhoami

app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hallo Service Management winter term 2022. My name is Thomas</p>"


@app.route("/")
def miniwhoami():
    return render_miniwhoami()