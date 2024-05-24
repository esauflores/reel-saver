from sqlalchemy.types import JSON

from . import db


class Reels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    caption = db.Column(db.Text, nullable=True)
    hashtags = db.Column(JSON, nullable=True)
    thumbnail_url = db.Column(db.String(255), nullable=True)
    saved_path = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Reel {self.url}>"
