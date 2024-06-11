from flask import Blueprint, send_from_directory, redirect, url_for

from flask_login import login_required

from helpers import env

storage_bp = Blueprint("storage", __name__)

STORAGE_PATH = env.get_env("STORAGE_PATH")


@storage_bp.route("/storage/reels/<path:filename>", methods=["GET"])
@login_required
def serve_reel(filename):
    return send_from_directory(STORAGE_PATH, f"reels/{filename}")


@storage_bp.route("/reel_video/<path:filename>", methods=["GET"])
@login_required
def serve_reel_video(filename):
    # download file automatically
    return send_from_directory(STORAGE_PATH, f"reels/{filename}", as_attachment=True)
