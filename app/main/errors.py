# -*- coding: UTF-8 -*-

from flask import render_template
from . import main
from datetime import datetime


current_time = datetime.utcnow()


# 401 error

@main.app_errorhandler(401)
def unauthorized_error(e):
    return render_template('error/401.html',
                           current_time=current_time), 404


# 403 error

@main.app_errorhandler(403)
def forbidden_error(e):
    return render_template('error/403.html',
                           current_time=current_time), 403


# 404 error

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html',
                           current_time=current_time), 404


# 500 error

@main.app_errorhandler(500)
def server_error(e):
    return render_template('error/500.html',
                           current_time=current_time), 500
