from app.utils.rendering import render


def redirect_routes(app, redirect_url: str):
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def redirect(path):
        return render("redirect.html", path=path, redirect_url=redirect_url)
