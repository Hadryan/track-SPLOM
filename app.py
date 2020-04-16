#! venv/bin/python

from flask import Flask, render_template, jsonify
from track_data import get_tracks

USERNAME = 'dtaylor072'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    data = get_tracks(USERNAME)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)