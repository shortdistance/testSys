# -*- coding: utf-8 -*-
from flask import redirect, g, session


def login_filter():
    if 'username' not in session or session['username'] is None:
        return redirect('/')
    else:
        g.user_id = session['userid']
        g.nick = session['nick']


def admin_filter():
    if 'username' not in session or session['username'] is None or 'isadmin' not in session or session[
        'isadmin'] is False:
        return redirect('/')
    else:
        g.user_id = session['userid']
        g.nick = session['nick']
