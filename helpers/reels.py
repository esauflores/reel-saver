# import logging
# import os
# import re

# import instagrapi
# import requests

# from helpers import env

# STORAGE_PATH = env.get_env("STORAGE_PATH")
# cl = None


# cl: instagrapi.Client = instagrapi.Client()

# logging.info("Logging in as %s", env.get_env("INSTAGRAM_USERNAME"))

# cl.load_settings("session.json")
# cl.login(env.get_env("INSTAGRAM_USERNAME"), env.get_env("INSTAGRAM_PASSWORD"))
# cl.get_timeline_feed()

# # cl.login(env.get_env("INSTAGRAM_USERNAME"), env.get_env("INSTAGRAM_PASSWORD"))
# # cl.dump_settings("session.json")

# logging.info("Logged in as %s", env.get_env("INSTAGRAM_USERNAME"))

# cl.delay_range = [1, 3]


# def save_reel_by_url(reel_url: str) -> tuple:
#     try:
#         reels_folder = os.path.join(STORAGE_PATH, "reels")
#         logging.info("Saving reel to %s", reels_folder)

#         # Save the reel
#         media_id = cl.media_pk_from_url(reel_url)
#         reel_path = cl.video_download(media_id, folder=reels_folder)

#         # Get the reel details
#         media_info = cl.media_info(media_id)
#         caption = media_info.caption_text if media_info.caption_text else ""
#         hashtags = re.findall(r"#\w+", caption)
#         thumbnail_url = str(media_info.thumbnail_url)

#         # download thumbnail
#         thumbnail_path = os.path.join(reels_folder, f"{media_id}.jpg")

#         with open(thumbnail_path, "wb") as f:
#             f.write(requests.get(thumbnail_url).content)

#         thumbnail_url = f"{media_id}.jpg"

#         logging.info("Reel saved to %s", reel_path)

#     except Exception as e:
#         logging.error("Error saving reel: %s", e)
#         return None

#     return media_id, caption, hashtags, thumbnail_url

import os

from helpers import env
import logging
import yt_dlp

STORAGE_PATH = env.get_env("STORAGE_PATH")


def get_reel_by_url(reel_url: str) -> tuple:
    try:
        reels_folder = os.path.join(STORAGE_PATH, "reels")
        logging.info("Saving reel to %s", reels_folder)

        ydl_opts = {
            "outtmpl": f"{reels_folder}/%(id)s.%(ext)s",
            "format": "best",
            "caption": True,
            "writethumbnail": True,
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }
            ],
            "logger": logging.getLogger("yt-dlp"),
            "cookiesfrombrowser": "chrome",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(reel_url, download=True)

        caption = info["description"]
        video_url = info["id"] + ".mp4"
        thumbnail_url = info["id"] + ".jpg"

        logging.info("Reel saved to %s", video_url)
        return caption, video_url, thumbnail_url

    except Exception as e:
        logging.error("Error saving reel: %s", e)
        return None


def validate_reel_url(reel_url: str):
    # validate that is a valid instagram reel url
    if "instagram.com" in reel_url:
        return True
