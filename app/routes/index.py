from app import app
import json
from flask import render_template, session
from operator import itemgetter

data = None
with open("data.json") as json_file:
    data = json.load(json_file)

rankings = data["rankings"]
total_matches = data["total_matches"]

for i in rankings:
    i["percentage"] = "{:.2f}".format(i["good"] * 100 / total_matches)


@app.route("/")
@app.route("/index")
def index():
    return render_template(
        "index.html",
        rankings=sorted(rankings, key=itemgetter("points", "good"), reverse=True),
        total_matches=total_matches,
    )
