from flask import Flask, request, send_from_directory, render_template, send_file
import json
import requests as rq
from urllib.parse import quote_plus
from random import randint
import pickle

with open('basically_firebase', 'rb') as f:
    faster_firebase = pickle.load(f)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return send_from_directory('static/', 'homepage.html')

@app.route('/browse')
def browse():
    params = request.args.to_dict()
    return json.dumps([ i for i in filter(lambda x: params['title'] in x['title'].lower(), faster_firebase.values())])

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
        faster_firebase[isbn] = formdata
    else:
        faster_firebase[str(randint(200, 200000))] = formdata
    with open('basically_firebase', 'wb') as f:
        pickle.dump(faster_firebase, f)
    return send_from_directory("static", "new_entry.html")


if __name__ == "__main__":
    app.run(debug=True)
