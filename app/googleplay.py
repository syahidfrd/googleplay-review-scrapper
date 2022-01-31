import json

from .helper import make_request
from config import ANDROID_PACKAGE_NAME
from .extensions import credentials
from google.auth.transport.requests import Request
from .models import PublishedReview


def _get_google_access_token():
    access_token = credentials.token
    if not credentials.valid:
        credentials.refresh(Request())
        access_token = credentials.token
    return access_token


def fetch_reviews():
    url = "https://www.googleapis.com/androidpublisher/v3/applications/{}/reviews".format(
        ANDROID_PACKAGE_NAME)

    headers = {"Content-Type": "application/json"}
    params = {"access_token": _get_google_access_token()}

    res = make_request(
        method="GET",
        url=url,
        headers=headers,
        params=params)

    return res


def reply_review(review_id, message):
    url = "https://www.googleapis.com/androidpublisher/v3/applications/{}/reviews/{}:reply".format(
        ANDROID_PACKAGE_NAME,
        review_id)

    headers = {"Content-Type": "application/json"}
    params = {"access_token": _get_google_access_token()}
    payload = {"replyText": message}

    res = make_request(
        method="POST",
        url=url,
        headers=headers,
        params=params,
        data=json.dumps(payload))

    return res


def is_first_run():
    result = False
    if PublishedReview.get_count_rows() == 0:
        result = True
    return result


def mark_as_published(review_id):
    published_review = PublishedReview(review_id=review_id)
    return published_review.save()
