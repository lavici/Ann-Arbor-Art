from flask import *
import flask

from extensions import connect_to_database

location = Blueprint('location', __name__, template_folder='templates')

@location.route('/location/<location_id>', methods=['GET'])
def location_route(location_id):
    db = connect_to_database()
    cur = db.cursor()
    cur.execute('SELECT * FROM Location WHERE locationID = %s', location_id)
    exists = cur.fetchall()
    if not exists:
        flask.abort(404)

    # if user is not logged in
    options = { 
        "logged_in":False,
    }

    return render_template("location.html", **options)

@location.route('/location_edit/<location_id>', methods=['GET', 'POST'])
def location_edit_route(location_id):
    db = connect_to_database()
    cur = db.cursor()
    cur.execute('SELECT * FROM Location WHERE locationID = %s', location_id)
    exists = cur.fetchall()
    if not exists:
        flask.abort(404)

    return render_template("location_edit.html")