# -*- coding: utf-8 -*-
# @Author: Kaushik S Kalmady
# @Date:   2018-10-22 21:36:24
# @Last Modified by:   kaushiksk
# @Last Modified time: 2018-10-24 11:30:16
import click
from pymongo import MongoClient, DESCENDING
from flask.cli import with_appcontext
import json
import os

<<<<<<< HEAD
mongo = MongoClient('mongodb://localhost:27017/')
||||||| merged common ancestors
mongo = MongoClient('mongodb://localhost:27017/')
=======
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
mongo = MongoClient('mongodb://localhost:27017/')

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    mongo.sahaay.users.drop()
    mongo.sahaay.login.drop()
    with open(os.path.join(PROJECT_ROOT, "credentials/login_credentials.json")) as f:
    	data = json.load(f)

    for item in data:
    	mongo.sahaay.login.insert(item)

    mongo.sahaay.login.create_index([("username", DESCENDING)])
    click.echo('Initialized the database.')	

def init_app(app):
    app.cli.add_command(init_db_command)

def get_maps_api_key():
	with open(os.path.join(PROJECT_ROOT, "credentials/gmap-api-key.txt")) as f:
		return f.read().strip()
>>>>>>> f19868c5ccb73c4251bd61f3a1745648e5a9eb68
