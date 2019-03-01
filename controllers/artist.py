from flask import *
from flask import request
import flask
import tempfile
import hashlib
import shutil
import requests
import os

from extensions import connect_to_database

artist = Blueprint('artist', __name__, template_folder='templates')

@artist.route('/artist/<artist_id>', methods=['GET'])
def artist_route(artist_id):
    db = connect_to_database()
    cur = db.cursor()
    cur.execute('SELECT * FROM Artist WHERE artistID = %s', artist_id)
    exists = cur.fetchall()
    if not exists:
    	flask.abort(404)

    # if user is not logged in
    options = { 
        "logged_in":False,
        "artist_id": artist_id,
    }

    return render_template("artist.html", **options)

@artist.route('/artist_edit/<artist_id>', methods=['GET', 'POST'])
def artist_edit_route(artist_id):
    db = connect_to_database()
    cur = db.cursor()
    cur.execute('SELECT * FROM Artist WHERE artistID = %s', artist_id)
    exists = cur.fetchall()
    if not exists:
        flask.abort(404)

    if request.form.get('upload_pfp', None) == "Upload Artist Image":
        """Upload photo to correct place."""
        dummy, temp_filename = tempfile.mkstemp()
        file = flask.request.files["file"]
        file.save(temp_filename)

        # Compute filename
        hash_txt = sha256sum(temp_filename)
        dummy, suffix = os.path.splitext(file.filename)
        # Name of the file uploaded to be saved in database
        hash_filename_basename = (hash_txt + suffix)
        if len(hash_filename_basename) > 64:
            hash_filename_basename = hash_filename_basename[:63]
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'static', 'img')
        hash_filename = os.path.join(upload_folder, hash_filename_basename)

        # Move temp file to permanent location
        shutil.move(temp_filename, hash_filename)

         # Upload to db to show instance
        db = connect_to_database()
        cur = db.cursor()
        cur.execute('UPDATE Artist SET image = %s WHERE artistID = %s', (hash_filename_basename, artist_id))

    # Loading details without any form submission occurs in javascript
    return render_template("artist_edit.html")

def sha256sum(filename):
    """Return sha256 hash of file content, similar to UNIX sha256sum."""
    content = open(filename, 'rb').read()
    sha256_obj = hashlib.sha256(content)
    return sha256_obj.hexdigest()
