from flask import (
    Blueprint, flash, redirect, g, render_template, request, session, url_for
)
from config import mongo

db = mongo["sahaay"]

bp = Blueprint('update', __name__, url_prefix='/update')

    
@bp.route('/', methods=['GET', 'POST'])
def update_inv():
    inventory = db["inventory"]

    # form to collect info    
    if request.method == 'POST':
        idx = request.form['idx'] 
        qty = request.form['qty']
        
        print idx, qty
        
        post = {"idx": idx, "qty": qty}
        post_id = inventory.insert_one(post).inserted_id
    
        data = inventory.find_one({'_id': post_id})
        print data
        
    return render_template('inventory-update.html')
        
