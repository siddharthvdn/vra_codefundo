# -*- coding: utf-8 -*-
# @Author: Kaushik S Kalmady
# @Date:   2018-10-23 00:13:02
# @Last Modified by:   kaushiksk
# @Last Modified time: 2018-10-23 00:35:35

import functools
from flask import (
    Blueprint, flash, redirect, g, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from config import mongo
from auth import login_required

bp = Blueprint('interact', __name__, url_prefix='/')


@bp.route('/')
@login_required
def index():
    return render_template('plain_page.html', user=g.user)