import requests
import json

from flask import current_app


def make_request(**kwargs):
    try:
        response = requests.request(**kwargs)
        request = response.request

        request_log = {}
        request_log["method"] = request.method
        request_log["url"] = request.url
        request_log["body"] = request.body
        request_log["status"] = response.status_code
        request_log["type"] = "OUTGOING_LOG"

        current_app.logger.info(json.dumps(request_log))
        response.raise_for_status()
        return response
    except requests.RequestException as err:
        raise err
