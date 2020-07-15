from flask import Flask, redirect, url_for
import logging
import logging.handlers

from .routes import *


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="ui/templates",
        static_folder="ui/static",
    )
    app.config.from_pyfile("config.py")

    # logging
    handler = logging.handlers.RotatingFileHandler(
        app.config["LOG_FILE"], maxBytes=app.config["LOG_SIZE"]
    )
    handler.setLevel(app.config["LOG_LEVEL"])
    handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(pathname)s at %(lineno)s]: %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
    )
    app.logger.addHandler(handler)

    with app.app_context():
        from .routes import auth, root

        app.register_blueprint(auth)
        app.register_blueprint(root)

    return app
