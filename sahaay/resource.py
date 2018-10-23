from flask import (
    Blueprint, flash, redirect, g, render_template, request, session, url_for
)
from config import mongo

db = mongo["sahaay"]

bp = Blueprint('resource', __name__, url_prefix='/resource')

    
@bp.route('/', methods=['GET', 'POST'])
def resource_request():

    # form to collect info    
    if request.method == 'POST':
        idx = request.form['idx'] 
        qty = request.form['qty']
        qty = int(qty)
        
        print idx, qty
        post = {'user':g.user, 'idx': idx }
        
        item = db.users.find_one({'user': g.user})

        item['location']

        neighbours = list( db.users.find(
                            {   location:
                                {   $near:
                                    {
                                        $geometry: item['location'],
                                        $minDistance: 0,
                                        $maxDistance: 5000
                                    }
                                }
                           }) )

        
        for neighbour in neighbours:            
            current = db.inventory.find_one({'user': neighbour['user'], 'idx': idx})
                if int(current['qty']) > qty:
                    #send request to this camp
                    print current['user']

        
    return render_template('inventory-update.html')
        

# db.users.find(
#    {
#      location:
#        { $near:
#           {
#             $geometry: { type: "Point",  coordinates: [ -73.9667, 40.78 ] },
#             $minDistance: 1000,
#             $maxDistance: 5000
#           }
#        }
#    }
# )
# 
# item['location']
# db.places.insert( {
#     name: "Central Park",
#    location: { type: "Point", coordinates: [ -73.97, 40.77 ] },
#    category: "Parks"
# } );