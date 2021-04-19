import os
from flask import Flask, Response, jsonify
from helper_functions import read_database


app = Flask(__name__)

PORT = 4444
UUID = '123456'

@app.route('/file/' + UUID + '/read/')
def read():
    resp = Response("")
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Content-Disposition'] = 'attachment; filename="cat.jpeg"'
    return resp

@app.route('/file/' + UUID + '/stat/')
def stat():
    mock = {'create_datetime': '2021-04-15',
    'size': '1024',
    'mimetype': 'image/jpeg',
    'name': 'cat.jpeg'}
    return jsonify(mock)

if __name__=="__main__":
    app.run(host=os.getenv('IP', 'localhost'), 
            port=int(os.getenv('PORT', PORT)))