function writeLocationToDOM(response) {
	var response_obj = response;
	document.getElementById("location-name-header").innerHTML = response_obj.location.locationName;
	document.getElementById("location-name-header").href = "https://www.google.com/maps/place/?q=place_id:" + response_obj.location.locationGooglePlaceID;
    document.getElementById("gmap_canvas").src = "https://www.google.com/maps/embed/v1/place?key=AIzaSyA-dGPJ-V1-Mr2TwzqQfHN_GdmK4PJNiig&q=place_id:" + response_obj.location.locationGooglePlaceID;
	document.getElementById("location-info-sidenav").innerHTML = response_obj.location.locationName;
    document.getElementById("location-description-sidenav").innerHTML = response_obj.location.locationDescription;
    var arts = response_obj.artwork.artwork;
    var arts_length = response_obj.artwork.artwork.length;
    var art_str = "";
    for (var i = 0; i < arts_length; i++) {
        art_str += "<a href=/art/" + arts[i].artID.toString() + ">" + arts[i].artTitle + "</a><br>";
    }
    document.getElementById("artworks-at-location-sidenav").innerHTML = art_str;
}

function renderLocation(locationID) {
	$.ajax('/api/location/' + locationID, {
		type: "GET",
		success: function(data, textStatus, jqXHR) {
	  		var response = data;
		  	writeLocationToDOM(response);
		},
		error: function(data, textStatus, jqXHR) {
	  		console.log("error");
		}
	});
}   