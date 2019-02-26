# TODO: Most recent results instead of fixed 9.
# TODO: Add the limit num results code found at the bottom of file.

# This is the API Backend implementation for getting all artwork information.
# Supported request is GET.
# 
# GET:		The GET method requests a representation of the specified 
# 			resource. Requests using GET should only retrieve data.

from flask import *
from extensions import *
from config import *

all_artworks_api = Blueprint('all_artworks_api', __name__, template_folder='templates')

# GET request.
@all_artworks_api.route('/api/artworks', methods=['GET'])
def all_artworks_get_route():
	db = connect_to_database()

	# Query artwork information to display in page.
	cursorArtworkQuery = db.cursor()
	cursorArtworkQuery.execute('SELECT * FROM Art ORDER BY artID DESC LIMIT 9')

	# Return error if no locations exist.
	if cursorArtworkQuery.rowcount == 0:
		errors = {
			"errors": [ { "title" : "The requested resource (artworks) could not be found" } ] 
		}
		return jsonify(errors), 404

	artworkInfo = cursorArtworkQuery.fetchall()

	artworks = []

	# Make a list with all the works queried and their respective artists. Each single entry will be 
	# sent as a JSON object formatted as below.
	for result in artworkInfo:
		artistID = result['artistID']

		# Query artist information to display in page.
		cursorArtistQuery = db.cursor()
		cursorArtistQuery.execute('SELECT * FROM Artist WHERE artistID = %s', artistID)

		# Return error if artist does not exist.
		if cursorArtistQuery.rowcount == 0:
			errors = {
				"errors": [ { "title" : "The requested resource (artist) could not be found" } ] 
			}
			return jsonify(errors), 404

		artistInfo = cursorArtistQuery.fetchall()

		currentArtwork = {
			"art": {
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
			},
			"artist": {
				"artistID": artistID,
				"artistName": artistInfo[0]['preferredName'],
				"artistHometown": artistInfo[0]['hometown'],
				"artistNationality": artistInfo[0]['nationality'],
				"artistBirth": artistInfo[0]['yearOfBirth'],
				"artistDeath": artistInfo[0]['yearOfDeath']
			}
		}

		artworks.append(currentArtwork)


	# Create the JSON object that will be sent to the front end.
	artworkJSON = {
		"artwork": artworks # This is a list of all artists (following the structure of 'artist' in artist.json)
	}

	return jsonify(artworkJSON)

	# resultLimit = request.args.get('limit')

	# if not resultLimit:
	# 	cursorLocationsQuery.execute('SELECT * FROM Art')
	# else:
	# 	try:
	# 	    limitValue = int(resultLimit)
	# 	    if limitValue < 1:
	# 	    	raise ValueError

	# 	    cursorLocationsQuery.execute('SELECT * FROM Art LIMIT %s')

	# 	except: #ValueError:
	# 	    errors = {
	# 	    	"errors": [ { "title" : "The provided limit of number of results is not an integer." } ] 
	# 	    }
	# 	    return jsonify(errors), 404

