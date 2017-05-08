# -*- coding: utf-8 -*-

from flask import Flask

from scripts.config import SECRET_KEY, DEBUG, SESSION_TIMEOUT
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config['SECRET_KEY'] = SECRET_KEY
    app.permanent_session_lifetime = timedelta(seconds=SESSION_TIMEOUT)
    app.Debug = DEBUG

    # 解决angularjs的模版冲突
    app.jinja_env.variable_start_string = '(('
    app.jinja_env.variable_end_string = '))'
    app.jinja_env.trim_blocks = True
    # 注册模块

    from .controllers import bp_login as login_blueprint
    from .controllers import bp_main as main_blueprint
    app.register_blueprint(login_blueprint)
    app.register_blueprint(main_blueprint)
    return app
