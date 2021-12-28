import os
import json


class Config:
    # secret key that will be used for securely signing the session cookie
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # specifies which type of session interface to use
    SESSION_TYPE = os.environ.get("SESSION_TYPE")
    # the database URI that should be used for the connection
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DB = os.environ.get("MYSQL_DB")

    if SECRET_KEY is None:
        # pylint: disable=W1514
        with open('./config.json') as config_file:
            config = json.load(config_file)

        SECRET_KEY = config.get('SECRET_KEY')
        SESSION_TYPE = config.get('SESSION_TYPE')
        SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
        MYSQL_HOST = config.get("MYSQL_HOST")
        MYSQL_USER = config.get("MYSQL_USER")
        MYSQL_PASSWORD = config.get("MYSQL_PASSWORD")
        MYSQL_DB = config.get("MYSQL_DB")
