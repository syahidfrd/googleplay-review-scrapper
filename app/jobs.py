from app import googleplay, qismo
from .extensions import scheduler
from config import JOB_INTERVAL
from .models import PublishedReview
from flask import current_app


@scheduler.task("interval", id="poll_reviews", seconds=int(JOB_INTERVAL))
def poll_google_play_reviews():
    with scheduler.app.app_context():
        current_app.logger.info("Jobs executed!")

        r = googleplay.fetch_reviews()
        reviews = r.json()["reviews"]
        if googleplay.is_first_run():
            """
            If we don't have any published reviews, then treat this as a baseline fetch, we won't post any
            reviews to qiscus multichannel, but new ones from now will be posted
            """
            for item in reviews:
                googleplay.mark_as_published(item["reviewId"])
        else:
            for item in reviews:
                published_review = PublishedReview.get_by_review_id(review_id=item["reviewId"])
                if not published_review:
                    current_app.logger.info("Found new review!")
                    qismo.send_custom_channel_message(
                        user_id=item["reviewId"].replace(":", "_"),
                        name=item["authorName"],
                        message=item["comments"][0]["userComment"]["text"])

                    googleplay.mark_as_published(review_id=item["reviewId"])
        pass
