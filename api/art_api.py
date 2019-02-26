# This is the API Backend implementation for the Artwork information.
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

art_api = Blueprint('art_api', __name__, template_folder='templates')

# GET request.
@art_api.route('/api/art/<artID>', methods=['GET'])
def art_get_route(artID):
	db = connect_to_database()

	# Query artwork information to display in page.
	cursorArtworkQuery = db.cursor()
	cursorArtworkQuery.execute('SELECT * FROM Art WHERE artID = %s', artID)

	# Return error if artwork does not exist.
	# if bool(artworkInfo) == False:
	if cursorArtworkQuery.rowcount == 0:
		errors = {
			"errors": [ { "title" : "The requested resource (artwork) could not be found" } ] 
		}
		return jsonify(errors), 404

	artworkInfo = cursorArtworkQuery.fetchall()

	artistID = artworkInfo[0]['artistID']
	mainImage = artworkInfo[0]['mainImage']
	locationID = artworkInfo[0]['locationID']
	isForSale = artworkInfo[0]['forSale']

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
	artistName = artistInfo[0]['preferredName']

	# Send back the correct name for the artist.
	if artistName is None:
		artistName = artistInfo[0]['name']

	# Query additional images to display in page.
	cursorImageQuery = db.cursor()
	cursorImageQuery.execute('SELECT * FROM Image WHERE artID = %s', artID)
	images = []

	# If there are additional images.
	if cursorImageQuery.rowcount != 0:
		imageInfo = cursorImageQuery.fetchall()

		# Make an array with all the images (filename.format).
		for result in imageInfo:
			currentImage = str(result['imageID']) + '.' + result['format']

			if not currentImage == mainImage:
				images.append(currentImage)

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

	# Initialize bid information to be equal to 0 (these values will change if isForSale).
	bidStartingAmount = 0
	bidHighestAmount = 0
	bidDirectSale = 0
	bidDeadline = 0
	bidIncrement = 0
	bidIncrementType = 0
	bidHighestID = 0

	# Check if artwork is for sale. If it is, get the artBid info, and update the variables 
	if isForSale == 1:
		# Query art bidding information to display in page.
		cursorArtBidQuery = db.cursor()
		cursorArtBidQuery.execute('SELECT * FROM ArtBid WHERE artID = %s', artID)

		if cursorArtBidQuery.rowcount == 0:
			errors = {
				"errors": 
					[ { "title" : "The requested resource (bidding information) could not be found" } ] 
			}
			return jsonify(errors), 404

		artBidInfo = cursorArtBidQuery.fetchall()

		bidStartingAmount = artBidInfo[0]['startingAmount']
		bidHighestAmount = artBidInfo[0]['highestBidAmount']
		bidDirectSale = artBidInfo[0]['directSale']
		# bidSold = artBidInfo[0]['sold']
		bidDeadline = artBidInfo[0]['deadline']
		bidIncrement = artBidInfo[0]['increment']
		bidIncrementType = artBidInfo[0]['incrementType']
		bidHighestID = artBidInfo[0]['highestBidID']

	# Query tag information to display in page.
	cursorTagIDQuery = db.cursor()
	cursorTagIDQuery.execute('SELECT * FROM TagMap WHERE artID = %s', artID)
	tags = []

	# If there are tags associated with artwork.
	if cursorTagIDQuery.rowcount != 0:
		tagIDs = cursorTagIDQuery.fetchall()

		# Make a list with all the tags (filename.format).
		for result in tagIDs:
			currentTagID = result['tagID']

			cursorTagQuery = db.cursor()
			cursorTagQuery.execute('SELECT * FROM Tags WHERE tagID = %s', currentTagID)

			# If there exists a tag associated with the corresponding tagID.
			if cursorTagQuery.rowcount != 0:
				currentTagInfo = cursorTagQuery.fetchall()

				currentTagName = currentTagInfo[0]['tagName']

				currentTag = {
					"tagID": currentTagID,
					"tagName": currentTagName
				}

				tags.append(currentTag)

	# Create the JSON object that will be sent to the front end.
	artworkJSON = {
		"art": {
			"artID": artID,
			"artTitle": artworkInfo[0]['title'],
			"artDescription": artworkInfo[0]['description'],
			"artType": artworkInfo[0]['type'],
			"artHeight": artworkInfo[0]['height'],
			"artWidth": artworkInfo[0]['width'],
			"artDepth": artworkInfo[0]['depth'],
			"artMedium": artworkInfo[0]['medium'],
			"artYear": artworkInfo[0]['year'],
			"artTags": tags # This is a list of tags (json objects)
		},
		"artist": {
			"artistID": artistID,
			"artistName": artistName,
			"artistHometown": artistInfo[0]['hometown'],
			"artistNationality": artistInfo[0]['nationality'],
			"artistBirth": artistInfo[0]['yearOfBirth'],
			"artistDeath": artistInfo[0]['yearOfDeath']
		},
		"location": {
			"locationID": locationID,
			"locationName": locationInfo[0]['name'],
			"locationCity": locationInfo[0]['city'],
			"locationLatitute": locationInfo[0]['latitude'],
			"locationLongitude": locationInfo[0]['longitude'],
			"googlePlaceID": locationInfo[0]['googlePlaceID']
		},
		"images": {
			"artMainImage": mainImage, # image_name.format
			"artOtherImages": images, # This is a list of image_names.format
		},
		"bids": {
			"artForSale": isForSale,
			"bidStartingAmount": bidStartingAmount,
			"bidHighestAmount": bidHighestAmount,
			"bidHighestID": bidHighestID,
			"bidDirectSale": bidDirectSale,
			#"bidSold": bidSold,
			"bidDeadline": bidDeadline,
			"bidIncrement": bidIncrement,
			"bidIncrementType": bidIncrementType # 0: percentage, 1: constant
		}
	}

	return jsonify(artworkJSON)


# PUT request to update art. 
@art_api.route('/api/art/<artID>', methods=['PUT'])
def art_put_route(artID):
	db = connect_to_database()

	# Create dictionary from the json object.
	dataObject = request.get_json()

	# Create variables with all the information coming from the 
	# front end.
	artID = dataObject["artID"]
	artistID = dataObject["artistID"]
	artTitle = dataObject["artTitle"]
	artDescription = dataObject["artDescription"]
	artType = dataObject["artType"]
	artHeight = dataObject["artHeight"]
	artWidth = dataObject["artWidth"]
	artDepth = dataObject["artDepth"]
	artMedium = dataObject["artMedium"]
	artYear = dataObject["artYear"]
	locationID = dataObject["locationID"]
	if dataObject["artMainImage"] != None: 
		artMainImage = dataObject["artMainImage"]
	artForSale = dataObject["artForSale"]

	cursorUpdateArt = db.cursor()
	if dataObject["artMainImage"] != None: 
		cursorUpdateArt.execute('UPDATE Art SET artistID = %s, title = %s, description = %s, type = %s, height = %s, width = %s, depth = %s, medium = %s, year = %s, locationID = %s, mainImage = %s, forSale = %s WHERE artID = %s', 
			(artistID, artTitle, artDescription, artType, artHeight, artWidth, artDepth, artMedium, artYear, locationID, artMainImage, artForSale, artID))
	else:
		cursorUpdateArt.execute('UPDATE Art SET artistID = %s, title = %s, description = %s, type = %s, height = %s, width = %s, depth = %s, medium = %s, year = %s, locationID = %s, forSale = %s WHERE artID = %s', 
			(artistID, artTitle, artDescription, artType, artHeight, artWidth, artDepth, artMedium, artYear, locationID, artForSale, artID))
	# TODO: Add error checking here.
	if request.method == 'POST':
		errors = {
			"errors": [ { "title" : "The requested resource (artist) could not be found." } ] 
		}
		return jsonify(errors), 404

	artworkJSON = art_get_route(artID)

	return artworkJSON, 200


# POST request to create art. 
@art_api.route('/api/art', methods=['POST'])
def art_post_route():
	db = connect_to_database()

	# Create dictionary from the json object.
	dataObject = request.get_json()

	# Create variables with all the information coming from the 
	# front end.
	artistID = dataObject["artistID"]
	artTitle = dataObject["artTitle"]
	artDescription = dataObject["artDescription"]
	artType = dataObject["artType"]
	artHeight = dataObject["artHeight"]
	artWidth = dataObject["artWidth"]
	artDepth = dataObject["artDepth"]
	artMedium = dataObject["artMedium"]
	artYear = dataObject["artYear"]
	locationID = dataObject["locationID"]
	artMainImage = dataObject["artMainImage"]
	artForSale = dataObject["artForSale"]

	cursorUpdateArt = db.cursor()
	cursorUpdateArt.execute('INSERT INTO Art SET artistID = %s, title = %s, description = %s, type = %s, height = %s, width = %s, depth = %s, medium = %s, year = %s, locationID = %s, mainImage = %s, forSale = %s', 
		(artistID, artTitle, artDescription, artType, artHeight, artWidth, artDepth, artMedium, artYear, locationID, artMainImage, artForSale))
	artID = cursorUpdateArt.lastrowid

	# TODO: Add error checking here.
	if request.method == 'PUT':
		errors = {
			"errors": [ { "title" : "The requested resource (artist) could not be found." } ] 
		}
		return jsonify(errors), 404

	artworkJSON = art_get_route(artID)

	return artworkJSON, 200
