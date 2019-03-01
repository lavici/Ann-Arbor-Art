function writeEditArtistToDOM(response) {
	var response_obj = response;
  
  // Artist Name
	// document.getElementById("artist-info-header").innerHTML = "<h1 id='artist-name-header'>" + response_obj.artist.artistPreferredName + "</h1>";
  document.getElementById('fullname').value = response_obj.artist.artistName;
  document.getElementById('prefname').value = response_obj.artist.artistPreferredName;

  // Artist Image
  if (response_obj.artist.artistImage != null) {
    document.getElementById("art-main-image").src = "../static/img/" + response_obj.artist.artistImage;
  }

  // Birth Dates
  if (response_obj.artist.artistBirth != null && response_obj.artist.artistDeath == null) {
    document.getElementById("birthyear").value = response_obj.artist.artistBirth;
  }
  else if (response_obj.artist.artistBirth == null && response_obj.artist.artistDeath != null) {
    document.getElementById("deathyear").value = response_obj.artist.artistDeath; 
  }
  else {
    document.getElementById("birthyear").value = response_obj.artist.artistBirth;
    document.getElementById("deathyear").value = response_obj.artist.artistDeath; 
  }

  // Nationality & Bio
  document.getElementById("edit-nationality").value = response_obj.artist.artistNationality;
  document.getElementById("artist-description-sidenav-edit").value = response_obj.artist.artistBio;
  document.getElementById("edit-hometown").value = response_obj.artist.artistHometown;

  // Artist Artwork
  var arts = response_obj.artwork.artwork;
  var arts_length = response_obj.artwork.artwork.length;
  var art_str = "";
  for (var i = 0; i < arts_length; i++) {
    art_str += "<a href=/art/" + arts[i].artID.toString() + '><img id="artist_art_thumb" src="../static/img/' + arts[i].artImage + '"</a>';
  }
  document.getElementById("artworks-by-artist").innerHTML = art_str;

}

function renderEditArtist(artistID) {
  $.ajax('/api/artist/' + artistID, {
    type: "GET",
    success: function(data, textStatus, jqXHR) {
      var response = data;
      writeEditArtistToDOM(response);
    },
    error: function(data, textStatus, jqXHR) {
      console.log("404 Error Redirect");
    }
  });
}

function createArtistEditJSON(artistID) {
  var edit_name = document.getElementById('fullname').value;
  var edit_pref = document.getElementById('prefname').value;
  var edit_birth = parseInt(document.getElementById("birthyear").value);
  var edit_death = parseInt(document.getElementById("deathyear").value);
  var edit_hometown = document.getElementById("edit-hometown").value;
  var edit_nationality = document.getElementById("edit-nationality").value;
  var edit_bio =  document.getElementById("artist-description-sidenav-edit").value;

  dataObject = {
    "artistID": artistID,
    "artistName": edit_name,
    "artistPreferredName": edit_pref,
    "artistHometown": edit_hometown,
    "artistNationality": edit_nationality,
    "artistBirth": edit_birth,
    "artistDeath": edit_death,
    "artistBio": edit_bio,
  }
  $.ajax({
      url: "/api/artist/" + artistID,
      type: 'PUT',    
      data: JSON.stringify(dataObject),
      contentType: 'application/json',
      success: function(result) {
          window.location.href = '/artist/' + artistID;
      },
      error: function() {
          //alert("Error saving data. Please try again.")
          console.log("error")
      }
  });
}