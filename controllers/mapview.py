from flask import *

from extensions import connect_to_database

mapview = Blueprint('mapview', __name__, template_folder='templates')

@mapview.route('/mapview', methods=['GET'])
def mapview_route():
        
    db = connect_to_database()

    # if user is not logged in
    options = { 
        "logged_in":False,
    }

    return render_template("index.html", **options)
