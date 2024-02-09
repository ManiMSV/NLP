from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['image_db']
fs = GridFS(db)

@app.route('/')
def index():
    files = fs.find()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    fs.put(file, filename=file.filename)
    return redirect(url_for('index'))

@app.route('/file/<id>')
def file(id):
    file = fs.get(ObjectId(id))
    return file.read()

if __name__ == "__main__":
    app.run(debug=True)