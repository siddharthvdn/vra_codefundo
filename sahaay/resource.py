from flask import (
    Blueprint, flash, jsonify, redirect, g, render_template, request, session, url_for
)
from .config import db
from pymongo import GEO2D

from bson.son import SON 
from bson import ObjectId
import datetime
from operator import itemgetter

from .config import SUPPLIES


bp = Blueprint('resource', __name__, url_prefix='/resource')

def repeat():
    loosers = db.requests.find({'qty':{'$gt': 0}})

    now = datetime.datetime.now()

    for looser in loosers:
        elapsed = divmod((now - looser['last_time']).total_seconds(), 60)[0]

        if elapsed > 60 or len(looser['to']) == 0:
            current = db.users.find_one({'username': looser['from']})

            query = {"location": SON([("$near", current['location']), ("$minDistance", looser['radius']), ("$maxDistance", looser['radius']+5000)])}
            neighbours = list(db.users.find(query))
            #print neighbours
            
            camps = looser['to']
            for neighbour in neighbours: 
                if not neighbour['username'] == looser['from']:  
                    #print neighbour['username']         
                    current = db.inventory.find_one({'username': neighbour['username'], 'idx': looser['idx']})
                    
                    if current is not None and current['qty'] > looser['qty']:
                        #send request to this camp
                        camps.append(current['username'])
                        #print current['username']   

            db.requests.update(
                {
                    '_id':ObjectId(looser['_id'])
                },
                {'$set': 
                    {
                        'to': camps,
                        'radius': looser['radius'] + 5000                        
                    }
                }, upsert=False)

    
@bp.route('/request', methods=['GET', 'POST'])
def request_resource():

    # form to collect info    
    if request.method == 'POST':
        idx = request.form['idx'] 
        qty = int(request.form['qty'])

        
        #print idx, qty
        post = {'username':g.user['username'], 'idx': idx }
        
        item = db.users.find_one({'username': g.user['username']})

        # db.users.create_index([('location', GEO2D)])
        #neighbours = list(db.users.find({'location': {"$near": item['location']}}).limit(3))
        query = {"location": SON([("$near", item['location']), ("$minDistance", 0), ("$maxDistance", 5000)])}
        neighbours = list(db.users.find(query))
        #print neighbours
        
        camps = []
        for neighbour in neighbours:   
            if not neighbour['username'] == g.user['username']:
                #print neighbour['username']         
                current = db.inventory.find_one({'username': neighbour['username'], 'idx': idx})
                
                if current is not None and current['qty'] > qty:
                    #send request to this camp
                    camps.append(current['username'])
                    #print current['username']


        request_post = {'from':g.user['username'], 
                        'idx': idx,
                        'qty': qty,
                        'ini_qty': qty,
                        'to':camps, 
                        'logs':[], 
                        'radius':5000, 
                        'ini_time':datetime.datetime.now(),
                        'last_time': datetime.datetime.now()
                        }

        id_ = db.requests.insert(request_post)

        return redirect('resource/order-summary/{}'.format(id_))

        
    return render_template('resource/request.html', supply=SUPPLIES)
        
@bp.route('/update', methods=['GET', 'POST'])
def update_resource():

    # form to collect info    
    if request.method == 'POST':
        idx = request.form['idx'] 
        qty = request.form['qty']
        qty = int(qty)

        #print idx, qty
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
        #print data

        flash("Inventory updated successfuly!", "success")
        

    return render_template('resource/update.html', supply=SUPPLIES)

@bp.route('/accept', methods=['POST'])
def accept_request():
    if request.method == 'POST':
        _id = request.form['_id']
        sup = int(request.form['supply'])

        item = db.requests.find_one({'_id': ObjectId(_id)})

        sup = min(sup, item['qty'])

        log = g.user['username'] + ' supplied ' + str(sup) + ' units of ' + item['idx']

        db.requests.update(
            {'_id': ObjectId(_id)},
            {'$set': {
                        'qty': item['qty'] - sup,
                        'last_time': datetime.datetime.now()
                    }}, 
            upsert=False)

        db.requests.update(
            {'_id': ObjectId(_id)},
            {'$push' : {'logs': log} },
            upsert=False)

        db.inventory.update(
            {
                'username': g.user['username'],
                'idx': item['idx']            
            },
            {'$inc': {'qty': -sup}},  
            upsert=False)

        return redirect('/resource/order-summary/{}'.format(_id))


@bp.route('/reject', methods=['POST'])
def reject_request():
    if request.method == 'POST':

        _id = request.form['_id']

        item = db.requests.find_one({'_id': ObjectId(_id)})

        log = g.user['username'] + ' rejected request for ' + str(int(item['qty'])) + ' units of ' + str(item['idx'])

        db.requests.update(
            {'_id': ObjectId(_id)},
            {'$push' : {'logs': log} }, 
            upsert=False)       

        return redirect(url_for("interact.index"))

@bp.route('/terminate', methods=['POST'])
def terminate_request():
    if request.method == 'POST':

        _id = request.form['_id']

        item = db.requests.find_one({'_id': ObjectId(_id)})

        log = g.user['username'] + ' terminated the request' 

        db.requests.update(
            {'_id': ObjectId(_id)},
            {'$push' : {'logs': log} }, 
            upsert=False)  

        db.requests.update(
            {'_id': ObjectId(_id)},
            {'$set': {'qty': 0}}, 
            upsert=False)  

        return redirect(url_for("interact.index"))

@bp.route('/order-summary/<order_id>', methods=['GET'])
def order_summary(order_id):
    item = db.requests.find_one({'_id': ObjectId(order_id)})

    item['_id'] = str(item['_id'])
    #print item
    curUserLoc = db.users.find_one({"username": g.user["username"]})["location"]
    fromUserLoc = db.users.find_one({"username": item["from"]})["location"]
    return render_template('resource/order-summary.html', item=item, source=curUserLoc, dest=fromUserLoc)

@bp.route('/myrequests')
def getmyrequests():
    username = g.user['username']
    requests = list(db.requests.find({"from": username}))
    #requests.sort(key=itemgetter("ini_time"), reverse=True)
    for req in requests:
        req["_id"] = str(req["_id"])

    return render_template("resource/myrequests.html", requests=requests)