from flask import Flask, request, send_from_directory, render_template, send_file
import pyrebase
import json
import requests as rq
from urllib.parse import quote_plus
from random import randint


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

@app.route('/download')
def download():
         send_file(request.args.get("file"), as_attachment=True)

@app.route('/browse')
def browse():
    books = [ db.child(i).get().val() for i in db.shallow().get().val() ]
    print(books)
    return render_template('browse.html', books=books)

@app.route('/styles/<path:path>')
def send_style_file(path):
    return send_from_directory('static/styles', path)

@app.route('/get_meta_data')
def find_metadata():
    params = request.args.to_dict()
    clean_keys = list(filter(lambda x: params[x], params.keys()))
    search_string_list = []
    for i in clean_keys:
        if i == 'title':
            search_string_list.append(f"intitle:{quote_plus(params[i])}")
        if i == 'author':
            search_string_list.append(f"inauthor:{quote_plus(params[i])}")
        if i == 'isbn':
            search_string_list.append(f"isbn:{quote_plus(params[i])}")
    r = rq.get('https://www.googleapis.com/books/v1/volumes', {
        "q" : "+".join(search_string_list)
    })
    results = json.loads(r.text)['items']
    results_dict = []
    for i in results:
        try:
            results_dict.append(
            {
            "title"          : i['volumeInfo']['title'],
            "authors"        : ", ".join(i['volumeInfo']['authors']),
            "isbn"           : i['volumeInfo']['industryIdentifiers'][0]['identifier'],
            "publisher"      : i['volumeInfo']['publisher'],
            "publishedDate"  : i['volumeInfo']['publishedDate'],
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
        return send_from_directory("static", "new_entry.html")
    formdata = request.form.to_dict()
    isbn = formdata['isbn']
    if isbn:
        db.child(isbn).set(formdata)
    else:
        db.child(randint(200, 200000)).set(formdata)
    return "<h1>Success</h1><br><a id='again' href='/new_entry'>Submit another?</a>"


if __name__ == "__main__":
    app.run(debug=True)
