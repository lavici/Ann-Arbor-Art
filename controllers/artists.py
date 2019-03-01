from flask import *

from extensions import connect_to_database

artists = Blueprint('artists', __name__, template_folder='templates')

@artists.route('/artists', methods=['GET'])
def artists_route():
        
    db = connect_to_database()

    # if user is not logged in
    options = { 
        "logged_in":False,
    }

    return render_template("artists.html", **options)
