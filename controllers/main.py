# for list.html

from flask import *

from extensions import connect_to_database

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def main_route():
        
    db = connect_to_database()

    # if user is not logged in
    options = { 
        "logged_in":False,
    }

    return render_template("list.html", **options)

@main.route('/bids/<artid>')
def all_bids(artid):
    db = connect_to_database()

    # if user is not logged in
    options = { 
        "logged_in":False,
        "artID":artid,
    }

    return render_template("all_bids.html", **options)
