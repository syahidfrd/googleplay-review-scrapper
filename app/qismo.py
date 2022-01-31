import json

from config import QISMO_APP_ID, QISMO_BASE_URL, CHANNEL_IDENTIFIER_KEY
from .helper import make_request


def send_custom_channel_message(user_id, name, message):
    url = "{}/{}/api/v2/custom_channel/send".format(QISMO_BASE_URL, QISMO_APP_ID)

    headers = {}
    headers["Content-Type"] = "application/json"

    payload = {}
    payload["identifier_key"] = CHANNEL_IDENTIFIER_KEY
    payload["user_id"] = user_id
    payload["name"] = name
    payload["message"] = message

    res = make_request(
        method="POST",
        url=url,
        headers=headers,
        data=json.dumps(payload))

    return res
