# TODO: SEND BACK ALSO TRANSACTION INFO.
# TODO: Figure out how the user that bidded is handled.

# This is the API Backend implementation for getting all bids for a specific artwork.
# Supported request is GET.
# 
# GET:		The GET method requests a representation of the specified 
# 			resource. Requests using GET should only retrieve data.

from flask import *
from extensions import *
from config import *

all_bids_api = Blueprint('all_bids_api', __name__, template_folder='templates')

# GET request.
@all_bids_api.route('/api/art/<artID>/bids', methods=['GET'])
def all_bids_get_route(artID):
	db = connect_to_database()

	# Query artwork information.
	cursorArtworkQuery = db.cursor()
	cursorArtworkQuery.execute('SELECT * FROM Art WHERE artID = %s', artID)

	# Return error if no artwork with this ID exists.
	if cursorArtworkQuery.rowcount == 0:
		errors = {
			"errors": [ { "title" : "The requested resource (artworks) could not be found" } ] 
		}
		return jsonify(errors), 404

	artworkInfo = cursorArtworkQuery.fetchall()

	# Query artBid information to display in page.
	cursorArtBidQuery = db.cursor()
	cursorArtBidQuery.execute('SELECT * FROM ArtBid WHERE artID = %s', artID)

	# Return error if no entry in ArtBid exists for this artID.
	if cursorArtBidQuery.rowcount == 0:
		errors = {
			"errors": [ { "title" : "The requested resource (bid information) could not be found. The artwork is not for sale or there is missing information." } ] 
		}
		return jsonify(errors), 404

	artBidInfo = cursorArtBidQuery.fetchall()

	# Query bids for the artwork to display in page.
	cursorBidsQuery = db.cursor()
	cursorBidsQuery.execute('SELECT * FROM Bid WHERE artID = %s', artID)
	bids = []

	# Add the bids if the artwork if the artwork already has bids (handles both 
	# direct sale and unbidded artworks).
	if cursorBidsQuery.rowcount != 0:
		bidInfo = cursorBidsQuery.fetchall()

		# Make a list with all the bids queried for the requested artwork. 
		# Each single entry will be sent as a JSON object formatted as below.
		for result in bidInfo:
			if result['validBid'] == 1:
				# Query user that bidded information.
				cursorUserQuery = db.cursor()
				cursorUserQuery.execute('SELECT * FROM User WHERE userID = %s', result['userID'])

				# Add bid information if the user exists.
				if cursorUserQuery.rowcount != 0:
					userInfo = cursorUserQuery.fetchall()

					currentBid = {
						"bid": {
							"bidID": result['bidID'],
							"bidAmount": result['amount']
						},
						"user": {
							"userID": userInfo[0]['userID'],
							"username": userInfo[0]['username'],
							"userFirstName": userInfo[0]['firstName'],
							"userLastName": userInfo[0]['lastName'],
							"userPhone": userInfo[0]['phone']
						}
					}

					bids.append(currentBid)

	# Create the JSON object that will be sent to the front end.
	bidsJSON = {
		"bids": bids # This is a list of all bids (following the above structure for each bid.
	}

	return jsonify(bidsJSON)
