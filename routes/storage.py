from flask import Blueprint, send_from_directory

from helpers import env

storage_bp = Blueprint("storage", __name__)

STORAGE_PATH = env.get_env("STORAGE_PATH")


@storage_bp.route("/storage/reels/<path:filename>", methods=["GET"])
def serve_reel_image(filename):
    return send_from_directory(STORAGE_PATH, f"reels/{filename}")
