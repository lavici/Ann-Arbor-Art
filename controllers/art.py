from flask import *
import flask

from extensions import connect_to_database

art = Blueprint('art', __name__, template_folder='templates')

@art.route('/art/<art_id>', methods=['GET'])
def art_route(art_id):
        
    db = connect_to_database()
    cur = db.cursor()
    cur.execute('SELECT * FROM Art WHERE artID = %s', art_id)
    exists = cur.fetchall()
    if not exists:
        flask.abort(404)

    # if user is not logged in
    options = { 
        "logged_in":False,
        "art_id": art_id,
    }

    return render_template("art.html", **options)

@art.route('/art_edit/<art_id>', methods=['GET', 'POST'])
def art_edit_route(art_id):
    db = connect_to_database()
    cur = db.cursor()
    cur.execute('SELECT * FROM Art WHERE artID = %s', art_id)
    exists = cur.fetchall()
    if not exists:
        flask.abort(404)

    return render_template("art_edit.html")
