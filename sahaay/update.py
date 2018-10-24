from flask import (
    Blueprint, flash, redirect, g, render_template, request, session, url_for
)
from config import mongo

db = mongo["sahaay"]

bp = Blueprint('update', __name__, url_prefix='/update')

    
@bp.route('/', methods=['GET', 'POST'])
def update_inventory():

    # form to collect info    
    if request.method == 'POST':
        idx = request.form['idx'] 
        qty = request.form['qty']
        qty = int(qty)

        print idx, qty

        item = db.inventory.find_one({'username': g.user['username'], 'idx': idx})
        
        if item is not None:
                qty = qty + item['qty']

                if qty<0:
                    # error = 'Quantity set to 0'
                    # flash(error, "error")
                    qty = 0

        post = {'username': g.user['username'], 'idx': idx}

        new_post = {'username': g.user['username'], 'idx': idx, 'qty': qty}

        db.inventory.update(post, new_post, True)

        data = db.inventory.find_one({'username': g.user['username'], 'idx': idx})
        print data
        
    return render_template('update-inventory.html')
        
