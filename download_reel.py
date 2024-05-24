import logging

from helpers import reels

logging.basicConfig(
    filename="app.log",  # Specify the file path where logs will be saved
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Specify the log message format
)

reel = "https://www.instagram.com/reel/C7VGAK_oZv_/"

reels.save_reel_by_url(reel)
