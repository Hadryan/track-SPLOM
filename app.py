#! venv/bin/python

from flask import Flask, render_template, jsonify
from get_tracks import get_data

USERNAME = 'dtaylor072'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    data = get_data(USERNAME)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)