from flask import Flask, render_template


# Create Flask instance
app = Flask(__name__)


# Create a route decorator
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/<name>')
def user(name):
    return "<h1>HELLO {}</h1>".format(name)