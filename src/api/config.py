from dotenv import load_dotenv
import os

load_dotenv()


class DevConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("MYSQL_DATABASE_URI")


class TestConfig:
    SECRET_KEY = os.getenv("TEST_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("MYSQL_DATABASE_URI")
