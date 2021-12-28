import os
import json


class Config:
    # secret key that will be used for securely signing the session cookie
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # specifies which type of session interface to use
    SESSION_TYPE = os.environ.get("SESSION_TYPE")
    # the database URI that should be used for the connection
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

    if SECRET_KEY is None:
        # pylint: disable=W1514
        with open('./config.json') as config_file:
            config = json.load(config_file)

        SECRET_KEY = config.get('SECRET_KEY')
        SESSION_TYPE = config.get('SESSION_TYPE')
        SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
