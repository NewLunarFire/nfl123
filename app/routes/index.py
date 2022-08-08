from app import app
from app.utils import render


@app.route("/")
@app.route("/index")
def index():
    return render(
        "index.html",
        rankings=[],
        total_matches=1,
    )
