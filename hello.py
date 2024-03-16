from flask import Flask, render_template


# Create Flask instance
app = Flask(__name__)


# Create a route decorator
@app.route('/')
def index():
    first_name = "Trey"
    return render_template("index.html", first_name=first_name)


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)