import webbrowser
from flask import Flask

app = Flask(__name__)


@app.route("/")
def homeHelper():
    return "hello"


@app.route("/login")
def loginHelper():
    return render_template("template.html")



if __name__ == "__main__":
    webbrowser.open_new("127.0.0.1:5000")
    app.debug = True
    app.run()