from flask import *

from extensions import connect_to_database

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/user/edit', methods=['GET'])
def user_edit_route():
        
    db = connect_to_database()

    # if user is not logged in
    options = { 
        "logged_in":False,
    }

    return render_template("user_edit.html")
@user.route('/user', methods=['GET'])
def user_route():
        
    db = connect_to_database()

    # if user is not logged in
    options = { 
        "logged_in":False,
    }

    return render_template("user_edit.html")

