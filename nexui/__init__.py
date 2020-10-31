'''NEXUI - Demo UI for nexo-in-the-cloud
'''
from flask import (
        Flask,
)
from . import blueprint_ui as ui

def create_app():
    '''Flask factory method
    '''
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(ui.bp)
    return app
