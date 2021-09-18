from flask import render_template
from app import app
from operator import itemgetter
import json

data = None
with open('data.json') as json_file:
    data = json.load(json_file)

rankings = data['rankings']
total_matches= data['total_matches']

for i in rankings:
    i['percentage'] = "{:.2f}".format(i['good'] * 100 / total_matches)

print(rankings)
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', rankings=sorted(rankings, key=itemgetter('points', 'good'), reverse=True), total_matches=total_matches)