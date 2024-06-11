import logging

from flask import Blueprint, redirect, render_template, request, url_for, session

from helpers import reels, navbar
from models import Reels, db

from flask_login import current_user, login_required


reels_bp = Blueprint("reels", __name__)


@reels_bp.route("/save_reel", methods=["POST"])
@login_required
def save_reel():
    try:
        reel_url = request.form.get("url")

        # validate reel url
        if not reels.validate_reel_url(reel_url):
            return "Invalid reel URL"

        caption, video_url, thumbnail_url = reels.get_reel_by_url(reel_url)
        new_reel = Reels(
            url=reel_url,
            caption=caption,
            video_url=video_url,
            thumbnail_url=thumbnail_url,
            user_id=current_user.id,
        )
        db.session.add(new_reel)
        db.session.commit()
    except Exception as e:
        logging.error("Error saving reel: %s", e)
        return f"Error saving reel: {e}"

    return redirect(url_for("reels.show_reels"))


@reels_bp.route("/reels/add", methods=["GET"])
@login_required
def add_reel():
    return render_template("reels/add_card.html", reels=reels)


@reels_bp.route("/reels/delete/<int:id>", methods=["GET"])
@login_required
def delete_reel(id):
    reel = Reels.query.get(id)
    db.session.delete(reel)
    db.session.commit()
    return redirect(url_for("reels.show_reels"))


@reels_bp.route("/reels", methods=["GET"])
@login_required
def show_reels():
    session["navbar_menu"] = navbar.get_navmenu()
    # reverse order of reels by current user id
    reels = (
        Reels.query.filter_by(user_id=current_user.id).order_by(Reels.id.desc()).all()
    )
    return render_template("reels/show_cards.html", reels=reels)
