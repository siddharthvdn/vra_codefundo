# -*- coding: utf-8 -*-
# @Author: Kaushik S Kalmady
# @Date:   2018-10-23 00:13:02
# @Last Modified by:   kaushiksk
# @Last Modified time: 2018-10-25 22:43:47

import functools
from flask import (
    Blueprint, flash, jsonify, redirect, g, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from config import mongo
from auth import login_required
from bson.son import SON
from pymongo import GEO2D
from operator import itemgetter

bp = Blueprint('interact', __name__, url_prefix='/')
db = mongo["sahaay"]

@bp.route('/')
@login_required
def index():
    username = g.user["username"]
    orders = list(db.requests.find({"to": username, "qty":{"$gt" : 0}}))
    requests = list(db.requests.find({"from": username, "qty":{"$gt" : 0}}))
    orders.sort(key=itemgetter("ini_time"), reverse=True)
    requests.sort(key=itemgetter("ini_time"), reverse=True)
    return render_template('dashboard.html', user=g.user, orders=orders, requests=requests)

@bp.route('/get-pie-data', methods=['GET'])
@login_required
def getpiedata():
    username = g.user["username"]
    items = list(db.inventory.find({"username": username}, {'_id': False}))

    #print items
    return jsonify({"data": items})


@bp.route('/get-local-map-data', methods=["GET"])
@login_required
def getmapdata():
    username = g.user["username"]
    curUser = db.users.find_one({"username": username}, {'_id': False})
    
    #db.users.create_index([('location', GEO2D)])
    query = {"location": SON([("$near", curUser['location'])])}
    localSites = list(db.users.find(query, {'_id': False}).limit(10))

    #print localSites
    return jsonify(localSites)

@bp.route('/test')
def test():
    return render_template('plain_page.html')

