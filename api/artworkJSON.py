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
		"bidHighestBidAmount": bidHighestBidAmount,
		"bidDirectSale": bidDirectSale,
		"bidDeadline": bidDeadline
	}
}