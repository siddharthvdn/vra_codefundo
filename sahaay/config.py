# -*- coding: utf-8 -*-
# @Author: Kaushik S Kalmady
# @Date:   2018-10-22 21:36:24
# @Last Modified by:   kaushiksk
# @Last Modified time: 2018-10-24 22:26:20
import click
from pymongo import MongoClient, DESCENDING, GEO2D
from flask.cli import with_appcontext
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
mongo = MongoClient('mongodb://localhost:27017/')

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    mongo.sahaay.users.drop()
    mongo.sahaay.login.drop()
    mongo.sahaay.inventory.drop()
    with open(os.path.join(PROJECT_ROOT, "credentials/login_credentials.json")) as f:
    	data = json.load(f)

    for item in data:
    	mongo.sahaay.login.insert(item)

    mongo.sahaay.login.create_index([("username", DESCENDING)])
    mongo.sahaay.users.create_index([('location', GEO2D)])
    click.echo('Initialized the database.')	    

def init_app(app):
    app.cli.add_command(init_db_command)

def get_maps_api_key():
	with open(os.path.join(PROJECT_ROOT, "credentials/gmap-api-key.txt")) as f:
		return f.read().strip()

with open(os.path.join(PROJECT_ROOT, "credentials/supplies_list.json")) as f:
    SUPPLIES = json.load(f)

