from flask import Flask, request
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
    
@app.route('/new_entry', METHOD=['GET', 'POST'])
def new_entry():
    if request.method == "GET":
        return send_from_directory("forms", "new_entry.html")
    print(request.form)
    pass


if __name__ == "__main__":
    app.run(debug=True)
    

