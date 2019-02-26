# TODO: Should we also send back locations? Do small pics also show that? CHANGE PUT AND POST (SHOULDNT HAVE ID).
# TODO: Add error checking for the SQL Update.
# TODO: Be more descriptive about error checking.
# TODO: Handle image
# TODO: FIX THE POST VS PUT FUNCTION ROUTES.

# This is the API Backend implementation for the Artist information.
# Supported requests are GET, POST, PUT, PATCH.
# 
# GET:		The GET method requests a representation of the specified 
# 			resource. Requests using GET should only retrieve data.
# POST:		The POST method is used to submit an entity to the specified 
# 			resource, often causing a change in state or side effects 
# 			on the server
# PUT:		The PUT method replaces all current representations of the 
# 			target resource with the request payload.
# PATCH:	The PATCH method is used to apply partial modifications 
# 			to a resource.

from flask import *
from extensions import *
from config import *

artist_api = Blueprint('artist_api', __name__, template_folder='templates')

# GET request.
@artist_api.route('/api/artist/<artistID>', methods=['GET'])
def artist_get_route(artistID):
	db = connect_to_database()

	# Query artist information to display in page.
	cursorArtistQuery = db.cursor()
	cursorArtistQuery.execute('SELECT * FROM Artist WHERE artistID = %s', artistID)

	# Return error if artist does not exist.
	# if bool(artworkInfo) == False:
	if cursorArtistQuery.rowcount == 0:
		errors = {
			"errors": [ { "title" : "The requested resource (artist) could not be found" } ] 
		}
		return jsonify(errors), 404

	artistInfo = cursorArtistQuery.fetchall()

	# Query information of the artwork made by artist to display in page.
	cursorArtworkQuery = db.cursor()
	cursorArtworkQuery.execute('SELECT * FROM Art WHERE artistID = %s', artistID)
	artwork = []

	# If there are pieces made by artist.
	if cursorArtworkQuery.rowcount != 0:
		artworkInfo = cursorArtworkQuery.fetchall()

		# Make a list with all the artwork made by the artist. Each single entry will be 
		# sent as a JSON object formatted as below.
		for result in artworkInfo:
			currentArtwork = {
				"artID": result['artID'],
				"artTitle": result['title'],
				"artDescription": result['description'],
				"artType": result['type'],
				"artHeight": result['height'],
				"artWidth": result['width'],
				"artDepth": result['depth'],
				"artMedium": result['medium'],
				"artYear": result['year'],
				"artImage": result['mainImage']
			}

			artwork.append(currentArtwork)

	# Create the JSON object that will be sent to the front end.
	artistJSON = {
		"artist": {
			"artistID": artistInfo[0]['artistID'],
			"artistName": artistInfo[0]['name'],
			"artistPreferredName": artistInfo[0]['preferredName'],
			"artistHometown": artistInfo[0]['hometown'],
			"artistNationality": artistInfo[0]['nationality'],
			"artistBirth": artistInfo[0]['yearOfBirth'],
			"artistDeath": artistInfo[0]['yearOfDeath'],
			"artistBio": artistInfo[0]['bio'],
			"artistImage": artistInfo[0]['image']
		},
		"artwork": {
			"artwork": artwork, # This is a list of artwork (following the structure of 'art' in artwork.json)
		}
	}

	return jsonify(artistJSON)


# PUT request to update artist. 
@artist_api.route('/api/artist/<artistID>', methods=['PUT'])
def artist_put_route(artistID):
	db = connect_to_database()

	# Create dictionary from the json object.
	dataObject = request.get_json()

	# Create variables with all the information coming from the 
	# front end.
	artistID = dataObject["artistID"]
	artistName = dataObject["artistName"]
	artistPreferredName = dataObject["artistPreferredName"]
	artistHometown = dataObject["artistHometown"]
	artistNationality = dataObject["artistNationality"]
	artistBirth = dataObject["artistBirth"]
	artistDeath = dataObject["artistDeath"]
	artistBio = dataObject["artistBio"]

	cursorUpdateArtist = db.cursor()
	cursorUpdateArtist.execute('UPDATE Artist SET name = %s, preferredName = %s, hometown = %s, nationality = %s, yearOfBirth = %s, yearOfDeath = %s, bio = %s WHERE artistID = %s', 
		(artistName, artistPreferredName, artistHometown, artistNationality, artistBirth, artistDeath, artistBio, artistID))

	# TODO: Add error checking here.
	if request.method == 'POST':
		errors = {
			"errors": [ { "title" : "The requested resource (artist) could not be found." } ] 
		}
		return jsonify(errors), 404

	artistJSON = artist_get_route(artistID)

	return artistJSON, 200


# POST request to create art. 
@artist_api.route('/api/artist', methods=['POST'])
def artist_post_route():
	db = connect_to_database()

	# Create dictionary from the json object.
	dataObject = request.get_json()

	# Create variables with all the information coming from the 
	# front end.
	artistName = dataObject["artistName"]
	artistPreferredName = dataObject["artistPreferredName"]
	artistHometown = dataObject["artistHometown"]
	artistNationality = dataObject["artistNationality"]
	artistBirth = dataObject["artistBirth"]
	artistDeath = dataObject["artistDeath"]
	artistBio = dataObject["artistBio"]

	cursorCreateArtist = db.cursor()
	cursorCreateArtist.execute('INSERT INTO Artist SET name = %s, preferredName = %s, hometown = %s, nationality = %s, yearOfBirth = %s, yearOfDeath = %s, bio = %s', 
		(artistName, artistPreferredName, artistHometown, artistNationality, artistBirth, artistDeath, artistBio))
	artistID = cursorCreateArtist.lastrowid

	# TODO: Add error checking here.
	if request.method == 'PUT':
		errors = {
			"errors": [ { "title" : "The requested resource (artist) could not be found." } ] 
		}
		return jsonify(errors), 404

	artistJSON = artist_get_route(artistID)

	return artistJSON, 200
