# This is the API Backend implementation for getting all artists information.
# Supported request is GET.
# 
# GET:		The GET method requests a representation of the specified 
# 			resource. Requests using GET should only retrieve data.

from flask import *
from extensions import *
from config import *
from operator import itemgetter

all_artists_api = Blueprint('all_artists_api', __name__, template_folder='templates')

# GET request.
@all_artists_api.route('/api/artists', methods=['GET'])
def all_artists_get_route():
	db = connect_to_database()

	# Query artists information to display in page.
	cursorArtistsQuery = db.cursor()
	cursorArtistsQuery.execute('SELECT * FROM Artist')

	# Return error if no artists exist.
	if cursorArtistsQuery.rowcount == 0:
		errors = {
			"errors": [ { "title" : "The requested resource (artists) could not be found" } ] 
		}
		return jsonify(errors), 404

	artistsInfo = cursorArtistsQuery.fetchall()

	artists = []

	# Make a list with all the artwork made by the artist. Each single entry will be 
	# sent as a JSON object formatted as below.
	for result in artistsInfo:
		currentArtist = {
			"artistID": result['artistID'],
			"artistName": result['name'],
			"artistPreferredName": result['preferredName'],
			"artistHometown": result['hometown'],
			"artistNationality": result['nationality'],
			"artistBirth": result['yearOfBirth'],
			"artistDeath": result['yearOfDeath'],
			"artistBio": result['bio'],
			"artistImage": result['image']
		}

		artists.append(currentArtist)

	sortedArtists = sorted(artists, key=itemgetter('artistPreferredName'))

	# Create the JSON object that will be sent to the front end.
	artistsJSON = {
		"artists": sortedArtists # This is a list of all artists (following the structure of 'artist' in artist.json)
	}

	return jsonify(artistsJSON)
