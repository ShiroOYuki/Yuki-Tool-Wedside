# https://ithelp.ithome.com.tw/articles/10222132
from flask import Flask
from flask import render_template
from flask import request
from flask_frozen import Freezer
import ascii_pic_main
import sys

app = Flask(__name__)
freezer = Freezer(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/test1")
def test1():
    return render_template("test1.html")


@app.route("/test2")
def test2():
    return render_template("test2.html")


@app.route("/ascii_pic", methods=["GET", "POST"])
def ascii_pic():
    if request.method == "POST":
        try:
            ascii_pic_main.main(request.form["pic_url"])
            return render_template("ascii_pic.html", alert="", getfile=True)
        except:
            return render_template("ascii_pic.html", alert="ERROR!", getfile=False)
    return render_template("ascii_pic.html", alert="", getfile=False)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        print("Building website...")
        freezer.freeze()
    else:
        app.run(debug=True, host="127.0.0.1", port=8000)
