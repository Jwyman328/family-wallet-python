from flask import Flask, request
from flask_cors import CORS
from src.views import balance_page, utxo_page, fees_api
from src.injection import ServiceContainer

# initialize struct log
from src.utils import logging  # noqa: F401, E261

import structlog

LOGGER = structlog.get_logger()
# TODO add env variables and configs for electrum server location / locations in general


class AppCreator:
    app = None

    @classmethod
    def create_app(cls) -> Flask:
        if cls.app is not None:
            return cls.app
        else:
            container = ServiceContainer()
            cls.app = Flask(__name__)
            CORS(
                cls.app,
                resources={r"/*": {"origins": "*"}},
                methods=["GET", "POST"],
                allow_headers=["Content-Type"],
            )

            cls.app.container = container
            cls.app.register_blueprint(balance_page)
            cls.app.register_blueprint(utxo_page)
            cls.app.register_blueprint(fees_api)

            return cls.app


def create_app() -> Flask:
    app = AppCreator.create_app()

    @app.before_request
    def log_request_info():
        LOGGER.info(
            "Request started",
            path=request.path,
            method=request.method,
            args=request.args,
            body=request.data,
        )

    @app.after_request
    def log_response_info(response):
        LOGGER.info(
            "Request completed",
            path=request.path,
            method=request.method,
            status_code=response.status_code,
        )
        return response

    return app
