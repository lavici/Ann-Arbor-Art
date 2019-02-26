# TODO: Look at artist file.
# TODO: Ask what kind of info should come with the Artwork object.
# TODO: Research on making JSON objects compliant to specific formats.

# This is the API Backend implementation for the Location information.
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

location_api = Blueprint('location_api', __name__, template_folder='templates')

# GET request.
@location_api.route('/api/location/<locationID>', methods=['GET'])
def location_get_route(locationID):
	db = connect_to_database()

	# Query location information to display in page.
	cursorLocationQuery = db.cursor()
	cursorLocationQuery.execute('SELECT * FROM Location WHERE locationID = %s', locationID)

	# Return error if location does not exist.
	if cursorLocationQuery.rowcount == 0:
		errors = {
			"errors": [ { "title" : "The requested resource (location) could not be found" } ] 
		}
		return jsonify(errors), 404

	locationInfo = cursorLocationQuery.fetchall()

	# Query information of the artwork in this location.
	cursorArtworkQuery = db.cursor()
	cursorArtworkQuery.execute('SELECT * FROM Art WHERE locationID = %s', locationID)
	artwork = []

	# If there are pieces in this location.
	if cursorArtworkQuery.rowcount != 0:
		artworkInfo = cursorArtworkQuery.fetchall()

		# Make a list with all the tags (filename.format).
		for result in artworkInfo:
			# Query information of the artist of the piece.
			cursorArtistQuery = db.cursor()
			cursorArtistQuery.execute('SELECT * FROM Artist WHERE artistID = %s', result['artistID'])

			# Return error if artist does not exist.
			if cursorLocationQuery.rowcount == 0:
				errors = {
					"errors": [ { "title" : "The requested resource (location) could not be found" } ] 
				}
				return jsonify(errors), 404


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
				"artMainImage": result['mainImage']
			}

			artwork.append(currentArtwork)

	# Create the JSON object that will be sent to the front end.
	locationJSON = {
		"location": {
			"locationID": locationInfo[0]['locationID'],
			"locationName": locationInfo[0]['name'],
			"locationAddress1": locationInfo[0]['address1'],
			"locationAddress2": locationInfo[0]['address2'],
			"locationCity": locationInfo[0]['city'],
			"locationState": locationInfo[0]['state'],
			"locationZipcode": locationInfo[0]['zipcode'],
			"locationType": locationInfo[0]['type'],
			"locationDescription": locationInfo[0]['description'],
			"locationLatitude": locationInfo[0]['latitude'],
			"locationLongitude": locationInfo[0]['longitude'],
			"locationGooglePlaceID": locationInfo[0]['googlePlaceID']
		},
		"artwork": {
			"artwork": artwork, # This is a list of artwork (following the structure of 'art' in artwork.json)
		}
	}

	return jsonify(locationJSON)


# PUT request to update artist. 
@location_api.route('/api/location/<locationID>', methods=['PUT'])
def location_put_route(locationID):
	db = connect_to_database()

	# Create dictionary from the json object.
	dataObject = request.get_json()

	# Create variables with all the information coming from the 
	# front end.
	locationID = dataObject["locationID"]
	locationName = dataObject["locationName"]
	locationAddress1 = dataObject["locationAddress1"]
	locationAddress2 = dataObject["locationAddress2"]
	locationCity = dataObject["locationCity"]
	locationState = dataObject["locationState"]
	locationZipcode = dataObject["locationZipcode"]
	locationType = dataObject["locationType"]
	locationDescription = dataObject["locationDescription"]
	locationLatitude = dataObject["locationLatitude"]
	locationLongitude = dataObject["locationLongitude"]
	locationGooglePlaceID = dataObject["locationGooglePlaceID"]

	cursorUpdateLocation = db.cursor()
	cursorUpdateLocation.execute('UPDATE Location SET name = %s, address1 = %s, address2 = %s, city = %s, state = %s, zipcode = %s, type = %s, description = %s, latitude = %s, longitude = %s, googlePlaceID = %s WHERE locationID = %s', 
		(locationName, locationAddress1, locationAddress2, locationCity, locationState, locationZipcode, 
			locationType, locationDescription, locationLatitude, locationLongitude, locationGooglePlaceID, locationID))

	# TODO: Add error checking here.
	if request.method == 'POST':
		errors = {
			"errors": [ { "title" : "The requested resource (location) could not be found." } ] 
		}
		return jsonify(errors), 404

	artistJSON = location_get_route(locationID)

	return artistJSON, 200

# POST request to create art. 
@location_api.route('/api/location', methods=['POST'])
def location_post_route():
	db = connect_to_database()

	# Create dictionary from the json object.
	dataObject = request.get_json()

	# Create variables with all the information coming from the front end.
	locationName = dataObject["locationName"]
	locationAddress1 = dataObject["locationAddress1"]
	locationAddress2 = dataObject["locationAddress2"]
	locationCity = dataObject["locationCity"]
	locationState = dataObject["locationState"]
	locationZipcode = dataObject["locationZipcode"]
	locationType = dataObject["locationType"]
	locationDescription = dataObject["locationDescription"]
	locationLatitude = dataObject["locationLatitude"]
	locationLongitude = dataObject["locationLongitude"]
	locationGooglePlaceID = dataObject["locationGooglePlaceID"]

	cursorCreateLocation = db.cursor()
	cursorCreateLocation.execute('INSERT INTO Location SET name = %s, address1 = %s, address2 = %s, city = %s, state = %s, zipcode = %s, type = %s, description = %s, latitude = %s, longitude = %s, googlePlaceID = %s', 
		(locationName, locationAddress1, locationAddress2, locationCity, locationState, locationZipcode, 
			locationType, locationDescription, locationLatitude, locationLongitude, locationGooglePlaceID))
	locationID = cursorCreateLocation.lastrowid
	# TODO: Add error checking here.
	if request.method == 'PUT':
		errors = {
			"errors": [ { "title" : "The requested resource (location) could not be found." } ] 
		}
		return jsonify(errors), 404

	locationJSON = location_get_route(locationID)

	return locationJSON, 200
