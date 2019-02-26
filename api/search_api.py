# This is the API Backend implementation for getting all locations information.
# Supported request is GET.
# 
# GET:		The GET method requests a representation of the specified 
# 			resource. Requests using GET should only retrieve data.

from flask import *
from extensions import *
from config import *
import requests
from .art_api import art_get_route
from .preprocess import tokenizeText, stemWords
from .porterStemmer import *

search_api = Blueprint('search_api', __name__, template_folder='templates')

# GET request.
@search_api.route('/api/search', methods=['GET'])
def search_get_route():
	query = request.args.get('q')
	print(query)
	if not query:
		errors = {
			"errors": [ { "title" : "No query term or parameter was specified" } ] 
		}
		return jsonify(errors), 404
	# preprocess text
	q1 = tokenizeText(query)
	query = " ".join(str(x) for x in q1)

	db = connect_to_database()

	# ARTWORKS --> title, tags

	# Query art title.
	cursorArtTitleQuery = db.cursor()
	cursorArtTitleQuery.execute('SELECT * FROM Art a1, Artist a2 WHERE a1.artistID = a2.artistID AND (MATCH (a1.title) AGAINST (%s IN NATURAL LANGUAGE MODE) OR MATCH (a2.name) AGAINST (%s IN NATURAL LANGUAGE MODE))', (query, query))
	artTitleInfo = cursorArtTitleQuery.fetchall()


	searchResults = []
	# Make a list with all the artwork made by the artist. Each single entry will be 
	# sent as a JSON object formatted as below.
	for result in artTitleInfo:
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

		searchResults.append(currentArtwork)

	# Create the JSON object that will be sent to the front end.
	searchResultsJSON = {
		"searchResults": searchResults # This is a list of all search results (following the structure of 'artist' in artist.json)
	}
	return jsonify(searchResultsJSON)


	# # # Query art tags
	# # cursorTagQuery.execute('SELECT * FROM Tags WHERE title LIKE %s', query)


	# # Query artist names.
	# cursorArtistNameQuery = db.cursor()
	# cursorArtistNameQuery.execute('SELECT * FROM Artist WHERE name LIKE %s OR preferredName LIKE %s', query, query)
	# ArtistNameInfo = cursorArtistNameQuery.fetchall()


	# # Return error if no locations exist.
	# if cursorLocationsQuery.rowcount == 0:
	# 	errors = {
	# 		"errors": [ { "title" : "The requested resource (locations) could not be found" } ] 
	# 	}
	# 	return jsonify(errors), 404

	# locationsInfo = cursorLocationsQuery.fetchall()
	
