import logging

from flask import Blueprint, redirect, render_template, request, url_for

from helpers import reels
from models import Reels, db

reels_bp = Blueprint("reels", __name__)


@reels_bp.route("/save_reel", methods=["POST"])
def save_reel():
    try:
        reel_url = request.form.get("url")
        print("reel_url", reel_url)
        reel_id, caption, hashtags, thumbnail_url = reels.save_reel_by_url(reel_url)
        new_reel = Reels(
            url=reel_url,
            saved_path=reel_id,
            caption=caption,
            hashtags=hashtags,
            thumbnail_url=thumbnail_url,
        )
        db.session.add(new_reel)
        db.session.commit()
    except Exception as e:
        logging.error("Error saving reel: %s", e)
        return f"Error saving reel: {e}"

    return redirect(url_for("home.home"))


@reels_bp.route("/reels", methods=["GET"])
def list_reels():
    reels = Reels.query.all()

    return str(*reels)


@reels_bp.route("/reels/add", methods=["GET"])
def add_reel():
    return render_template("reels/add_card.html", reels=reels)


@reels_bp.route("/reels/delete/<int:id>", methods=["GET"])
def delete_reel(id):
    reel = Reels.query.get(id)
    db.session.delete(reel)
    db.session.commit()
    return redirect(url_for("home.home"))
