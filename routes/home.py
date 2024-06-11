from flask import Blueprint, render_template, session

from helpers import navbar
from models import Reels

home_bp = Blueprint("home", __name__)


@home_bp.route("/", methods=["GET"])
def home():
    session["navbar_menu"] = navbar.get_navmenu()
    # reverse order of reels
    reels = Reels.query.order_by(Reels.id.desc()).all()
    return render_template("index.html", reels=reels)
