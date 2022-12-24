from flask import Flask
from .views import hello_world
import bdkpython as bdk
from flask import g
from .injection import ServiceContainer


def create_app() -> Flask:
    container = ServiceContainer()
    app = Flask(__name__)
    app.container = container
    app.register_blueprint(hello_world.hello_world_page)

    return app
