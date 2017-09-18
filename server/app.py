from flask import Flask

from server.db.database import ReplayDatabase


def register_blueprints(app, prefix='/'):
    from server.api import player
    app.register_blueprint(player.api, url_prefix=prefix)


def prepare_app():
    prepared_app = Flask(__name__)
    register_blueprints(prepared_app)
    prepared_app.db = ReplayDatabase()
    return prepared_app


app = prepare_app()
