# -*- coding: utf-8 -*-
# @Author: Kaushik S Kalmady
# @Date:   2018-10-22 21:49:59
# @Last Modified by:   kaushiksk
# @Last Modified time: 2018-10-24 22:27:00
import functools
from flask import (
    Blueprint, flash, redirect, g, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from .config import mongo

db = mongo["sahaay"]

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = session["username"]
        email = request.form['email']
        longitude = float(request.form['longitude'])
        latitude = float(request.form['latitude'])
        
        error = None

        if not username:
            error = 'Username is required.'
        elif db.users.find_one({"username": username}) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            user_data = {'username': username,
                         'email': email,
                         'location': [longitude, latitude]}

            db.users.insert(user_data)

            db.login.update_one(
                    {"username": username},
                    {
                        '$set':{
                            'verified': True
                        }
                    })
            flash("Details Updated Successfully!", "success")
            return redirect(url_for('interact.index'))

        flash(error, "error")

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.login.find_one({"username": username})
        error = None

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['username'] = user['username']
            flash("Welcome {}!".format(user['username']), "success")

            print 
            if not user["verified"]:
                return render_template('auth/register.html') 
                
            return redirect(url_for('interact.index'))

        flash(error, 'error')

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('interact.index'))


@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')
    from . import config
    if username is None:
        g.user = None
    else:
        g.user = db.users.find_one({"username": username})
    g.api_key = config.get_maps_api_key()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view