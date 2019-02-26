# TODO: Send back all artwork information for each location.

# This is the API Backend implementation for getting all locations information.
# Supported request is GET.
# 
# GET:		The GET method requests a representation of the specified 
# 			resource. Requests using GET should only retrieve data.

from flask import *
from extensions import *
from config import *
from operator import itemgetter

all_locations_api = Blueprint('all_locations_api', __name__, template_folder='templates')

# GET request.
@all_locations_api.route('/api/locations', methods=['GET'])
def all_locations_get_route():
	db = connect_to_database()

	# Query locations information to display in page.
	cursorLocationsQuery = db.cursor()
	cursorLocationsQuery.execute('SELECT * FROM Location')

	# Return error if no locations exist.
	if cursorLocationsQuery.rowcount == 0:
		errors = {
			"errors": [ { "title" : "The requested resource (locations) could not be found" } ] 
		}
		return jsonify(errors), 404

	locationsInfo = cursorLocationsQuery.fetchall()

	locations = []

	# Make a list with all the artwork made by the artist. Each single entry will be 
	# sent as a JSON object formatted as below.
	for result in locationsInfo:
		currentLocation = {
			"locationID": result['locationID'],
			"locationName": result['name'],
			"locationAddress1": result['address1'],
			"locationAddress2": result['address2'],
			"locationCity": result['city'],
			"locationState": result['state'],
			"locationZipcode": result['zipcode'],
			"locationType": result['type'],
			"locationDescription": result['description'],
			"locationLatitude": result['latitude'],
			"locationLongitude": result['longitude'],
			"locationGooglePlaceID": result['googlePlaceID']
		}

		locations.append(currentLocation)

	# Create the JSON object that will be sent to the front end.
	locationsJSON = {
		"locations": locations # This is a list of all artists (following the structure of 'artist' in artist.json)
	}

	return jsonify(locationsJSON)
