from flask import Flask
from flask_cors import CORS
from src.views import balance, utxos
from src.injection import ServiceContainer


# set up hot reloading
# TODO fix why I get 0 tests to run doing $ python -m unittest
# TODO set up nvim pyhton linting and formatting -x
# TODO hook up black /some typing in vscode
# TODO set up some tests with unittest and pytest. - x
# TODO add env variables and configs for electrum server location / locations in general
# TODO set up docker postgres
# set up alembric / sqlalchamey and some models.
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
            cls.app.register_blueprint(balance.balance_page)
            cls.app.register_blueprint(utxos.utxo_page)

            return cls.app


def create_app() -> Flask:
    return AppCreator.create_app()
