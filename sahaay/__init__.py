import os

from flask import Flask
from flask import render_template, request

def create_app(test_config=None):
    app = Flask(__name__,  instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import auth, interact, resource
    app.register_blueprint(auth.bp)
    app.register_blueprint(interact.bp)
    app.register_blueprint(resource.bp)
    
    from . import config
    config.init_app(app)
    return app
