from flask import Blueprint, send_from_directory

sw_blueprint = Blueprint("serviceworker", __name__)

@sw_blueprint.route("/serviceWorker.js")
def serve_service_worker():
    return send_from_directory("static", "js/serviceWorker.js")
