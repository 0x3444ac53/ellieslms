from flask import Flask, request, send_from_directory, render_template
import pyrebase
import json
import requests as rq

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

app = Flask(__name__)

@app.route('/')
def hello_world():
    return send_from_directory('static/', 'landing_page.html')

@app.route('/styles/<path:path>')
def send_style_file(path):
    return send_from_directory('static/styles', path)

@app.route('/get_meta_data')
def find_metadata():
    title = request.args.get('title')
    print(title)
    r = rq.get(f'https://www.googleapis.com/books/v1/volumes?q=intitle:{title}')
    results = json.loads(r.text)['items']
    results_dict = []
    for i in results:
        try:
            results_dict.append(
            {
            "title"      : i['volumeInfo']['title'],
            "authors"    : ", ".join(i['volumeInfo']['authors']),
            "isbn"       : i['volumeInfo']['industryIdentifiers'][0]['identifier'],
            }
            )
        except KeyError:
            continue
    return json.dumps(results_dict)

@app.route('/js/<path:path>')
def sildnd_js(path):
    return send_from_directory('static/js', path)

@app.route('/new_entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == "GET":
        return send_from_directory("forms", "new_entry.html")
    db.child('books').push(request.form.to_dict())


if __name__ == "__main__":
    app.run(debug=True)
