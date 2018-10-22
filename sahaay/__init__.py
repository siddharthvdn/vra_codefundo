import os

from flask import Flask
from flask import render_template, request

from pymongo import MongoClient

def create_app(test_config=None):
    app = Flask(__name__,  instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    
    client = MongoClient()    
    db = client["database"]
    inventory = db["inventory"]

    # form to collect info
    @app.route('/', methods=['GET', 'POST'])
    def form():
        if request.method == 'POST':
            idx = request.form['idx'] 
            qty = request.form['qty']
            
            print idx, qty
            
            post = {"idx": idx, "qty": qty}
            post_id = inventory.insert_one(post).inserted_id
            
            #print inventory.find(post_id)
        
            data = inventory.find_one({'_id': post_id})
            print data
            
    	return render_template('inventory-update.html')
        
        

    return app
