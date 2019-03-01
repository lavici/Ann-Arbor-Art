function writeArtistToDOM(response) {
	var response_obj = response;
  
  // Artist Name
	document.getElementById("artist-info-header").innerHTML = "<h1 id='artist-name-header'>" + response_obj.artist.artistPreferredName + "</h1>";
  if (response_obj.artist.artistPreferredName != response_obj.artist.artistName) {
    document.getElementById("artist-info-sidenav-page").innerHTML = response_obj.artist.artistPreferredName + "<p>(" + response_obj.artist.artistName + ")</p>";
  }
  else {
    document.getElementById("artist-info-sidenav-page").innerHTML = response_obj.artist.artistName;
  }

  // Artist Image
  if (response_obj.artist.artistImage != null) {
    document.getElementById("art-main-image").src = "../static/img/" + response_obj.artist.artistImage;
  }

  // Birth Dates
  if (response_obj.artist.artistBirth == null && response_obj.artist.artistDeath == null) {
    document.getElementById("birth-year").innerHTML = "";
    document.getElementById("death-year").innerHTML = ""; 
  }
  else if (response_obj.artist.artistBirth != null && response_obj.artist.artistDeath == null) {
    document.getElementById("birth-year").innerHTML = " Year of Birth - " + response_obj.artist.artistBirth;
    document.getElementById("death-year").innerHTML = ""; 
  }
  else if (response_obj.artist.artistBirth == null && response_obj.artist.artistDeath != null) {
    document.getElementById("birth-year").innerHTML = "";
    document.getElementById("death-year").innerHTML = "Year of Death - " + response_obj.artist.artistDeath; 
  }
  else {
    document.getElementById("birth-year").innerHTML = " Year of Birth - " + response_obj.artist.artistBirth;
    document.getElementById("death-year").innerHTML = "Year of Death - " + response_obj.artist.artistDeath; 
  }

  // Nationality & Bio
  if (response_obj.artist.artistNationality != null) {
    document.getElementById("creation-date-sidenav").innerHTML = response_obj.artist.artistNationality;
  }
  if (response_obj.artist.artistBio != null) {
    document.getElementById("artist-description-sidenav").innerHTML = response_obj.artist.artistBio;
  }
  if (response_obj.artist.artistHometown != null) {
    document.getElementById("hometown-sidenav").innerHTML = response_obj.artist.artistHometown;
  }
  
  // Artist Artwork
  var arts = response_obj.artwork.artwork;
  var arts_length = response_obj.artwork.artwork.length;
  var art_str = "";
  for (var i = 0; i < arts_length; i++) {
    art_str += "<a href=/art/" + arts[i].artID.toString() + '><img id="artist_art_thumb" src="../static/img/' + arts[i].artImage + '"</a>';
  }
  document.getElementById("artworks-by-artist").innerHTML = art_str;

}

function renderArtist(artistID) {
  $.ajax('/api/artist/' + artistID, {
    type: "GET",
    success: function(data, textStatus, jqXHR) {
      var response = data;
      writeArtistToDOM(response);
    },
    error: function(data, textStatus, jqXHR) {
      console.log("404 Error Redirect");
    }
  });
}