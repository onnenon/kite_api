import os

from spylogger import get_logger

LOGGER = get_logger(log_level="DEBUG")

DEBUG = True
SECRET_KEY = os.getenv(
    "API_SECRET", "6150645367566B59703373367638792F423F4528482B4D6251655468576D5A71"
)
# DATABASE
SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    os.getenv("API_DB_USERNAME", "admin"),
    os.getenv("API_DB_PASSWORD", "pass"),
    os.getenv("API_DB_HOST", "localhost"),
    os.getenv("API_DB_PORT", "5432"),
    os.getenv("API_DB_NAME", "forum_db"),
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

FORUM_ADMIN = {
    "username": os.getenv("FORUM_ADMIN", "admin"),
    "password": os.getenv("FORUM_ADMIN_PASS", "pass"),
}
