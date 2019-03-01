function renderEditLocation(locationID) {
	$.ajax('/api/location/' + locationID, {
		type: "GET",
		success: function(data, textStatus, jqXHR) {
	  		var response = data;
		  	writeEditLocationToDOM(response);
		},
		error: function(data, textStatus, jqXHR) {
	  		console.log("error");
		}
	});
}

function writeEditLocationToDOM(response) {
	var response_obj = response;
	document.getElementById("location-name-header").innerHTML = "Edit Location";
    document.getElementById("gmap_canvas").src = "https://www.google.com/maps/embed/v1/place?key=AIzaSyA-dGPJ-V1-Mr2TwzqQfHN_GdmK4PJNiig&q=place_id:" + response_obj.location.locationGooglePlaceID;
	document.getElementById("location-info-sidenav").value = response_obj.location.locationName;
	document.getElementById("location-description-sidenav").value = response_obj.location.locationDescription;
    document.getElementById("location-addr1").value = response_obj.location.locationAddress1;
    document.getElementById("location-addr2").value = response_obj.location.locationAddress2;
    document.getElementById("location-city").value = response_obj.location.locationCity;
    document.getElementById("location-state").value = response_obj.location.locationState;
    document.getElementById("location-zip").value = response_obj.location.locationZipcode;
    document.getElementById("location-type").value = response_obj.location.locationType;
    document.getElementById("location-lat").value = response_obj.location.locationLatitude;
    document.getElementById("location-long").value = response_obj.location.locationLongitude;
    document.getElementById("location-google").value = response_obj.location.locationGooglePlaceID;


}

function submitLocationEditJSON(locationID) {
	var edit_name = document.getElementById('location-info-sidenav').value;
	var edit_description = document.getElementById("location-description-sidenav").value;
	var edit_addr1 = document.getElementById("location-addr1").value;
    var edit_addr2 = document.getElementById("location-addr2").value;
    var edit_city = document.getElementById("location-city").value;
    var edit_state = document.getElementById("location-state").value;
    var edit_zip = parseInt(document.getElementById("location-zip").value);
    var edit_type = document.getElementById("location-type").value;
    var edit_lat = document.getElementById("location-lat").value;
    var edit_long = document.getElementById("location-long").value;
    var edit_google = document.getElementById("location-google").value;

	dataObject = {
		"locationID": locationID,
		"locationName": edit_name,
		"locationAddress1": edit_addr1,
		"locationAddress2": edit_addr2,
		"locationCity": edit_city,
		"locationZipcode": edit_zip,
		"locationType": edit_type,
		"locationDescription": edit_description,
		"locationLatitude": edit_lat,
		"locationLongitude": edit_long,
		"locationGooglePlaceID": edit_google,
		"locationState": edit_state,
	}

	$.ajax({
		url: "/api/location/" + locationID,
		type: 'PUT',    
		data: JSON.stringify(dataObject),
		contentType: 'application/json',
		success: function(result) {
		  window.location.href = '/location/' + locationID;
		},
		error: function() {
		  //alert("Error saving data. Please try again.")
		  console.log("error")
		}
  	});
}