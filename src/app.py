from flask import Flask
from .views import hello_world
from .injection import ServiceContainer

# TODO hook up black /some typing in vscode
# TODO set up some tests with unittest and pytest. - x
# TODO add env variables and configs for electrum server location / locations in general
# TODO clean up imports, why so many init files / folders.
# TODO set up docker postgres
# set up alembric / sqlalchamey and some models.
def create_app() -> Flask:
    container = ServiceContainer()
    app = Flask(__name__)
    app.container = container
    app.register_blueprint(hello_world.hello_world_page)

    return app
