function newArtist() {
  var new_name = document.getElementById('new-fullname').value;
  var new_pref = document.getElementById('new-prefname').value;
  var new_birth = document.getElementById('new-birth-year').value;
  var new_death = document.getElementById('new-death-year').value;
  var new_birth = document.getElementById('new-birth-year').value;
  var new_hometown = document.getElementById('new-hometown').value;
  var new_nationality = document.getElementById('new-nationality').value;
  var new_bio = document.getElementById('new-bio').value; 

  if (new_death === '') {
    new_death = null;
  }
  if (new_birth == '') {
    new_birth = null;
  }

  dataObject = {
    "artistName": new_name,
    "artistPreferredName": new_pref,
    "artistHometown": new_hometown,
    "artistNationality": new_nationality,
    "artistBirth": new_birth,
    "artistDeath": new_death,
    "artistBio": new_bio,
  }

  $.ajax({
    url: "/api/artist",
    type: 'POST',    
    data: JSON.stringify(dataObject),
    contentType: 'application/json',
    success: function(result) {
      document.getElementById('status-code').innerHTML = "<div class='alert alert-success' role='alert'><h4 class='alert-heading'>New Artist Created!</h4></div>";
    },
    error: function() {
      alert("Error saving data. Please try again.");
    }
  });
}

function newArt() {
  var new_title = document.getElementById('new-art').value;
  var new_type = document.getElementById('art-type').value;
  var new_height = parseFloat(document.getElementById('new-height').value);
  var new_width = parseFloat(document.getElementById('new-width').value);
  var new_depth = parseFloat(document.getElementById('new-depth').value);
  var new_medium = document.getElementById('new-medium').value;
  var new_year = parseInt(document.getElementById('new-year').value);
  var artist_select = document.getElementById("choose-artist");
  var new_artist = parseInt(artist_select.options[artist_select.selectedIndex].value);
  var location_select = document.getElementById("choose-location");
  var new_location = parseInt(location_select.options[location_select.selectedIndex].value);
  var sell_select = document.getElementById("choose-sale");
  var new_sale = parseInt(sell_select.options[sell_select.selectedIndex].value);
  var new_bio = document.getElementById("new-bio").value;

  dataObject = {
    "artistID": new_artist,
    "artTitle": new_title,
    "artDescription": new_bio,
    "artType": new_type,
    "artHeight": new_height,
    "artWidth": new_width,
    "artDepth": new_depth,
    "artMedium": new_medium,
    "artYear": new_year,
    "locationID": new_location,
    "artMainImage": "no_artist_img.png",
    "artForSale": new_sale,
  }

  $.ajax({
    url: "/api/art",
    type: 'POST',    
    data: JSON.stringify(dataObject),
    contentType: 'application/json',
    success: function(result) {
      document.getElementById('status-code').innerHTML = "<div class='alert alert-success' role='alert'><h4 class='alert-heading'>New Art Created!</h4></div>";
    },
    error: function() {
      alert("Error saving data. Please try again.");
    }
  });
}

function newLocation() {
  var new_location = document.getElementById('new-locname').value;
  var new_lat = parseFloat(document.getElementById('new-lat').value);
  var new_long = parseFloat(document.getElementById('new-long').value);
  var new_google = document.getElementById('new-google').value;
  var new_loc_addr1 = document.getElementById('new-addr1').value;
  var new_loc_addr2 = document.getElementById('new-addr2').value;
  var new_city = document.getElementById('new-city').value;
  var new_state = document.getElementById('new-state').value;
  var new_zip = document.getElementById('new-zip').value;
  var new_loc_desc = document.getElementById('new-desc').value;

  dataObject = {
    "locationName": new_location,
    "locationAddress1": new_loc_addr1,
    "locationAddress2": new_loc_addr2,
    "locationCity": new_city,
    "locationState": new_state,
    "locationZipcode": new_zip,
    "locationType": 0,
    "locationDescription": new_loc_desc,
    "locationLatitude": new_lat,
    "locationLongitude": new_long,
    "locationGooglePlaceID": new_google,
  }

  $.ajax({
    url: "/api/location",
    type: 'POST',    
    data: JSON.stringify(dataObject),
    contentType: 'application/json',
    success: function(result) {
      document.getElementById('status-code').innerHTML = "<div class='alert alert-success' role='alert'><h4 class='alert-heading'>New Location Created!</h4></div>";
    },
    error: function() {
      alert("Error saving data. Please try again.");
    }
  });
}