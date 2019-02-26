# This is the API Backend implementation for the Bid information.
# Supported requests are GET, POST, PUT, PATCH.
# 
# POST:		The POST method is used to submit an entity to the specified 
# 			resource, often causing a change in state or side effects 
# 			on the server

from flask import *
from extensions import *
from config import *

bid_api = Blueprint('bid_api', __name__, template_folder='templates')

# POST request to create bid. 
@bid_api.route('/api/art/<artID>/bid', methods=['POST'])
def bid_post_route(artID):
	db = connect_to_database(artID)

	# Create dictionary from the json object.
	dataObject = request.get_json()
	success = False

	username = dataObject['username'] # This is the email gotten from their Google Account info
	amount = dataObject['amount']

	# Check if user 
	try:
		bidAmount = int(amount)
	except ValueError:
		errors = {
			"errors": [ { "title" : "The provided amount is not a number." } ] 
		}
		return jsonify(errors), 404

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


	# Query user that bidded information.
	cursorUserQuery = db.cursor()
	cursorUserQuery.execute('SELECT * FROM User WHERE username = %s', username)

	# Return error if no entry in User exists for this userID.
	if cursorUserQuery.rowcount == 0:
		errors = {
			"errors": [ { "title" : "The requested resource (user) could not be found." } ] 
		}
		return jsonify(errors), 404

	userInfo = cursorUserQuery.fetchall()
	userID = userInfo[0]['userID']


	# Query artBid information to display in page.
	cursorArtBidQuery = db.cursor()
	cursorArtBidQuery.execute('SELECT * FROM ArtBid WHERE artID = %s', artID)

	# Return error if never for sale or no entry in ArtBid exists for this artID.
	if artworkInfo[0]['forSale'] == 0 or cursorArtBidQuery.rowcount == 0:
		errors = {
			"errors": [ { "title" : "The requested resource (bid information) could not be found. Not for sale." } ] 
		}
		return jsonify(errors), 404

	artBidInfo = cursorArtBidQuery.fetchall()

	if artBidInfo[0]['sold']:
		errors = {
			"errors": [ { "title" : "You are not allowed to bid for this artwork. It has already been sold." } ] 
		}
		return jsonify(errors), 403

	# Add bid and mark as sold if its direct sale
	if artBidInfo[0]['directSale']:
		if bidAmount >= artBidInfo['startingAmount']:
			cursorAddBid = db.cursor()
			cursorAddBid.execute('INSERT INTO Bid SET artID = %s, userID = %s, amount = %s, validBid = 1', 
				(artID, userID, bidAmount))
			bidID = cursorAddBid.lastrowid

			cursorUpdateArtBid = db.cursor()
			cursorUpdateArtBid.execute('UPDATE ArtBid SET sold = 1, highestBidID = %s, highestBidAmount = %s WHERE artID = %s', 
				(bidID, bidAmount, artID))

			success = True
	# Add bid and update the highest bid information
	else:
		# Calculate the min acceptable value to bid
		nextHighestBid = artBidInfo['highestBidAmount']
		if artBidInfo['incrementType'] == 0:
			nextHighestBid += artBidInfo['increment'] * artBidInfo['highestBidAmount']
		else:
			nextHighestBid += artBidInfo['increment']

		if bidAmount >= nextHighestBid:
			cursorAddBid = db.cursor()
			cursorAddBid.execute('INSERT INTO Bid SET artID = %s, userID = %s, amount = %s, validBid = 1', 
				(artID, userID, bidAmount))
			bidID = cursorAddBid.lastrowid

			cursorUpdateArtBid = db.cursor()
			cursorUpdateArtBid.execute('UPDATE ArtBid SET highestBidID = %s, highestBidAmount = %s WHERE artID = %s', 
				(bidID, bidAmount, artID))

			success = True

	if success:
		return 200

	else:
		errors = {
			"errors": [ { "title" : "You are not allowed to bid for this artwork. It has already been sold." } ] 
		}
		return jsonify(errors), 404 
