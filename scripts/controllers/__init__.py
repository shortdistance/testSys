# -*- coding: utf-8 -*-
from flask import Blueprint
from scripts.models import database

bp_login = Blueprint('login', __name__)
bp_main = Blueprint('main', __name__)

from scripts.controllers.filters import login_filter

bp_main.before_request(login_filter)

from . import home, project, task, team, issue, upload
from . import user, admin, case, runcase, setting, comment, monitor


@bp_main.after_request
def close_session_after_request(response):
    database.close_session()
    return response
