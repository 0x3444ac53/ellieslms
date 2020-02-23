from flask import Flask, request, send_from_directory, render_template
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyCW5qlAvA2_OJkBwThVmYBx5dTclukt-KE",
  "authDomain": "biblilgbt.firebaseapp.com",
  "databaseURL": "https://biblilgbt.firebaseio.com",
  "projectId": "biblilgbt",
  "storageBucket": "biblilgbt.appspot.com",
  "messagingSenderId": "169445643632",
  "appId": "1:169445643632:web:135cef1726227e0c4d6bb5",
  "measurementId": "G-SRSQXYC19F"
};

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
users = db.child("harry potter").get()

print("tes!!t")
print(users.val())

app = Flask(__name__)

@app.route('/')
def hello_world():
    print("test")
    print(users.val())
    return "<h1>Hello Wolrd</h1>"

@app.route('/styles/<path:path>')
def send_style_file(path):
    return send_from_directory('static/styles', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == "GET":
        return send_from_directory("forms", "new_entry.html")
    return str(request.form.get('title'))


if __name__ == "__main__":
    app.run(debug=True)
    

