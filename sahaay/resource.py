from flask import (
    Blueprint, flash, redirect, g, render_template, request, session, url_for
)
from config import mongo
from pymongo import GEO2D

from bson.son import SON

import datetime

db = mongo["sahaay"]

bp = Blueprint('resource', __name__, url_prefix='/resource')

def repeat():
    loosers = db.requests.find({'status':0})

    now = datetime.datetime.now()

    for looser in loosers:
        elapsed = divmod((now - looser['last_time']).total_seconds(), 60)[0]

        if elapsed > 60 or len(looser['to']) == 0:
            query = {"location": SON([("$near", looser['location']), ("$minDistance", looser['radius']), ("$maxDistance", looser['radius']+5000)])}
            neighbours = list(db.users.find(query))
            print neighbours
            
            camps = looser['to']
            for neighbour in neighbours:   
                print neighbour['username']         
                current = db.inventory.find_one({'username': neighbour['username'], 'idx': looser['idx']})
                
                if current is not None and current['qty'] > looser['qty']:
                    #send request to this camp
                    camps.append(current['user'])
                    print current['username']   

            db.requests.update_one(
                {
                    '_id':looser['_id']
                },
                {'$set': 
                    {
                        'to': camps,
                        'radius': looser['radius'] + 5000,
                        'last_time': datetime.datetime.now()
                    }
                }, upsert=False)

    
@bp.route('/request', methods=['GET', 'POST'])
def request_resource():

    # form to collect info    
    if request.method == 'POST':
        idx = request.form['idx'] 
        qty = int(request.form['qty'])

        
        print idx, qty
        post = {'username':g.user['username'], 'idx': idx }
        
        item = db.users.find_one({'username': g.user['username']})

        item['location']

        db.users.create_index([('location', GEO2D)])
        #neighbours = list(db.users.find({'location': {"$near": item['location']}}).limit(3))
        query = {"location": SON([("$near", item['location']), ("$minDistance", 0), ("$maxDistance", 5000)])}
        neighbours = list(db.users.find())
        print neighbours
        
        camps = []
        for neighbour in neighbours:   
            print neighbour['username']         
            current = db.inventory.find_one({'username': neighbour['username'], 'idx': idx})
            
            if current is not None and current['qty'] > qty:
                #send request to this camp
                camps.append(current['username'])
                print current['username']

        request_post = {'from':g.user['username'], 
                        'idx': idx,
                        'qty': qty,
                        'to':camps, 
                        'status':0, 
                        'donor':None, 
                        'radius':5000, 
                        'ini_time':datetime.datetime.now(),
                        'last_time': datetime.datetime.now()
                        }

        db.requests.insert(request_post)

        
    return render_template('resource/request.html')
        
@bp.route('/update', methods=['GET', 'POST'])
def update_resource():

    # form to collect info    
    if request.method == 'POST':
        idx = request.form['idx'] 
        qty = request.form['qty']
        qty = int(qty)

        print idx, qty
        #print g.user["username"], session["username"]
        item = db.inventory.find_one({'username': g.user['username'], 'idx': idx})
        
        if item is not None:
                qty = qty + item['qty']

                if qty < 0:
                    error = "You have only {} items of this type".format(item['qty'])
                    flash(error, "error")
                    return render_template('resource/update.html')

        post = {'username': g.user['username'], 'idx': idx}

        new_post = {'username': g.user['username'], 'idx': idx, 'qty': qty}

        db.inventory.update(post, new_post, True)

        data = db.inventory.find_one({'username': g.user['username'], 'idx': idx})
        print data

        flash("Inventory updated successfuly!", "success")
        
    return render_template('resource/update.html')


