import os

from dotenv import load_dotenv

ENV_LOADED = False  # Check if the environment variables have been loaded


# Try to get the environment variable
def get_env(variable: str, default=None) -> str:
    global ENV_LOADED

    # Load the environment variables if they have not been loaded
    if not ENV_LOADED:
        load_dotenv()
        ENV_LOADED = True

    # Get the environment variable
    return os.environ.get(variable, default)
