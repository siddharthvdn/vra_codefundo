# -*- coding: utf-8 -*-
# @Author: Kaushik S Kalmady
# @Date:   2018-10-22 21:49:59
# @Last Modified by:   kaushiksk
# @Last Modified time: 2018-10-23 12:43:36
import functools
from flask import (
    Blueprint, flash, redirect, g, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from config import mongo

db = mongo["sahaay"]

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        longitude = request.form['longitude']
        latitude = request.form['latitude']
        
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.users.find_one({"username": username}) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            user_data = {'username': username,
                         'password': generate_password_hash(password),
                         'email': email,
                         'longitude': longitude,
                         'latitude': latitude}

            db.users.insert(user_data)
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.users.find_one({"username": username})
        error = None

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['username'] = user['username']
            print user
            return redirect(url_for('interact.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('interact.index'))


@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = db.users.find_one({"username": username})


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view