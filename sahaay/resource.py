from flask import (
    Blueprint, flash, jsonify, redirect, g, render_template, request, session, url_for
)
from config import mongo
from pymongo import GEO2D

from bson.son import SON

import datetime

db = mongo["sahaay"]

bp = Blueprint('resource', __name__, url_prefix='/resource')

def repeat():
    loosers = db.requests.find({'qty':{$gt: 0} }})

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
                camps.append(current['user'])
                print current['username']

        request_post = {'from':g.user['username'], 
                        'idx': idx,
                        'qty': qty,
                        'to':camps, 
                        'logs':None, 
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

        item = db.inventory.find_one({'username': g.user['username'], 'idx': idx})
        
        if item is not None:
                qty = qty + item['qty']

                if qty < 0:
                    error = "Quantity cannot be negative"
                    flash(error, "error")
                    return render_template('resource/update.html')

        post = {'username': g.user['username'], 'idx': idx}

        new_post = {'username': g.user['username'], 'idx': idx, 'qty': qty}

        db.inventory.update(post, new_post, True)

        data = db.inventory.find_one({'username': g.user['username'], 'idx': idx})
        print data
        
    return render_template('resource/update.html')

@bp.route('/accept', methods=['POST'])
def accept_request():
    if request.method == 'POST':
        _id = request.json['id']
        sup = request.json['supply']

        item = db.requests.find_one({'_id': _id})

        sup = min(sup, item['qty'])

        log = g.user['username'] + ' supplied ' + str(sup) + ' units of' + item['idx']

        db.requests.update(
            {
                '_id': _id
            },
            {'$set': 
                {
                    'qty': item['qty'] - sup
                    {$push : {'logs': log} }
                }
            }, upsert=False)

        db.inventory.update(
            {
                'username': g.user['username'],
                'idx': item['idx']            
            },
            {'$inc':
                {
                    'qty': -sup
                }
            },  upsert=False)

        return jsonify({'supplied': sup})

    return render_template('resource/accept.html')



@bp.route('/reject', methods=['POST'])
def reject_request():
    if request.method == 'POST':
        _id = request.json['id']

        item = db.requests.find_one({'_id': _id})

        log = g.user['username'] + ' rejected request for ' + str(sup) + ' units of' + item['idx']

        db.requests.update(
            {
                '_id': _id
            },
            {'$set': 
                {
                    {$push : {'logs': log} }
                }
            }, upsert=False)       

        return jsonify({'supplied': 0})


    return render_template('resource/accept.html')