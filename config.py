"""Configure env variables."""
from os import environ, path
from dotenv import load_dotenv

if path.exists(".env"):
    load_dotenv(verbose=True)


class Config:
    """Set Flask configuration variables from .env file."""

    # General Flask Config
    STEAM_API_KEY = environ.get('STEAM_API_KEY')
    ENV = environ.get('ENV')
    TEMPLATES_AUTO_RELOAD = environ.get('TEMPLATES_AUTO_RELOAD')
    DEBUG = environ.get('DEBUG')