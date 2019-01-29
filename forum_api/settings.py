import os
import spylogger

LOGGER = spylogger.get_logger()

# DATABASE
SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    os.getenv("LAMP_DB_USERNAME"),
    os.getenv("LAMP_DB_PASSWORD"),
    os.getenv("LAMP_DB_HOST", "localhost"),
    os.getenv("LAMP_DB_PORT", "5432"),
    os.getenv("LAMP_DB_NAME"),
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
