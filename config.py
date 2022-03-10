import os


class Config:
    # secret key that will be used for securely signing the session cookie
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # specifies which type of session interface to use
    SESSION_TYPE = os.environ.get("SESSION_TYPE")

    # the database URI that should be used for the connection
    uri = os.environ.get('DATABASE_URL')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = uri
    else:
        raise ValueError("Incorrectly formatted postgres URL")

    # Flask-SQLAlchemy will not track modification of objects and emit signals
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MySQL config settings
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DB = os.environ.get("MYSQL_DB")
