from flask import *

from extensions import connect_to_database

search = Blueprint('search', __name__, template_folder='templates')

@search.route('/search', methods=['GET'])
def search_route():
        
    db = connect_to_database()
    # if user is not logged in
    options = { 
        "logged_in":False,
    }


    return render_template("search.html", **options)
