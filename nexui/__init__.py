from flask import (
        Flask,
)

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from . import blueprint_ui as ui
    app.register_blueprint(ui.bp)

    return app
