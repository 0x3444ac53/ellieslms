from flask import Flask

app = Flask(__main__)

@app.route('/')
def hello_world():
    return "<h1>Hello Wolrd</h1>"
