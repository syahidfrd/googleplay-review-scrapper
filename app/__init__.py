"""
App init module.
"""
import logging
import time
import json

from flask import Flask, request, g
from werkzeug.exceptions import HTTPException
from http import HTTPStatus
from flask.logging import default_handler
from .extensions import *
from . import googleplay


def create_app():
    """
    An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config")

    # handler configuration
    logging.getLogger("werkzeug").disabled = True
    default_handler.setLevel(logging.DEBUG)
    default_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))

    # init extensions
    db.init_app(app)
    scheduler.init_app(app)

    with app.app_context():
        # Removes all inherited from db.Model table
        db.drop_all()
        # Creates all inherited from db.Model table
        db.create_all()

    # running jobs scheduler
    from . import jobs # noqa: F401
    scheduler.start()

    @app.before_request
    def before_request():
        g.start = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(g, "start") and request.path != "/favicon.ico":
            now = time.time()
            body = request.get_json(force=True) if request.is_json else dict(request.form)

            request_log = {}
            request_log["method"] = request.method
            request_log["path"] = request.path
            request_log["params"] = dict(request.args)
            request_log["body"] = body
            request_log["status"] = response.status_code
            request_log["latency"] = round(now - g.start, 2)
            request_log["ip"] = request.headers.get("X-Forwarded-For", request.remote_addr)
            request_log["host"] = request.host.split(":", 1)[0]
            request_log["type"] = "REQUEST_LOG"

            app.logger.info(json.dumps(request_log))

        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(str(e))
        error_data = {}
        error_data["status"] = HTTPStatus.INTERNAL_SERVER_ERROR
        error_data["message"] = "internal server error"

        if isinstance(e, HTTPException):
            error_data["status"] = e.code
            error_data["message"] = e.description

        return error_data, error_data["status"]

    @app.route("/")
    def index():
        return {"status": 200, "message": "api up and running!"}

    @app.route("/webhook/custom_channel", methods=["POST"])
    def webhook_custom_channel():
        json_data = request.get_json(force=True)
        message = json_data["payload"]["message"]["text"]
        participants = json_data["payload"]["room"]["participants"]
        customer = next((item for item in participants if item["email"].startswith("gp_")), None)
        review_id = customer["email"].replace("_", ":", 1) if customer else None
        if review_id:
            googleplay.reply_review(review_id=review_id, message=message)

        return {"status": 200}

    return app
