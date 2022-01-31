from .extensions import db
from sqlalchemy.exc import SQLAlchemyError


class BaseModel(db.Model):
    """
    Abstract Model.
    Define the base model for all other models.
    """

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())

    def as_dict(self):
        # return data as python dictionary
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()

    def update(self):
        return db.session.commit()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()


class PublishedReview(BaseModel):
    review_id = db.Column(db.String, nullable=False, index=True)

    def __repr__(self):
        return "<PublishedReview id:{}>".format(self.id)

    @classmethod
    def get_count_rows(cls):
        return cls.query.count()

    @classmethod
    def get_by_review_id(cls, review_id):
        return cls.query.filter_by(review_id=review_id).first()
