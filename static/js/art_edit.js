function writeEditArtToDOM(response) {
  var response_obj = response;
  console.log(response_obj);
  document.getElementById("art-title-header").innerHTML = "Edit Artwork";
  document.getElementById("title").value = response_obj.art.artTitle;
  document.getElementById("artist").value = response_obj.artist.artistID;

  document.getElementById("location").value = response_obj.location.locationID;
  document.getElementById("creation-date-sidenav").value = response_obj.art.artYear;
  document.getElementById("medium-sidenav").value = response_obj.art.artMedium;
  document.getElementById("art-description-sidenav").value = response_obj.art.artDescription;
  document.getElementById("art-main-image").src = "../static/img/" + response_obj.images.artMainImage;
  document.getElementById("bid").value = response_obj.bids.artForSale;

  var loc_all = ""
  $.ajax('/api/locations', {
    type: "GET",
    success: function(data, textStatus, jqXHR) {
      var response = data.locations.length;
      for (var i = 0; i < response; i++) {
        loc_all += "<option>" + data.locations[i].locationID + " - " + data.locations[i].locationName + "</option>";
      }
      document.getElementById("location").innerHTML = loc_all
    },
    error: function(data, textStatus, jqXHR) {
      console.log("error");
    }
  });
  
  var artist_all = ""
  $.ajax('/api/artists', {
    type: "GET",
    success: function(data, textStatus, jqXHR) {
      var response = data.artists.length;
      for (var i = 0; i < response; i++) {
        artist_all += "<option>" + data.artists[i].artistID + " - " + data.artists[i].artistName + "</option>";
      }
      document.getElementById("artist").innerHTML = artist_all
    },
    error: function(data, textStatus, jqXHR) {
      console.log("error");
    }
  });

}

function renderEditArt(artID) {
  $.ajax('/api/art/' + artID, {
    type: "GET",
    success: function(data, textStatus, jqXHR) {
      var response = data;
      writeEditArtToDOM(response);
    },
    error: function(data, textStatus, jqXHR) {
      console.log("error");
    }
  });
}

function createArtEditJSON(artID) {
  var edit_title = document.getElementById('title').value;
  var artist_select = document.getElementById("artist");
  var edit_artist = parseInt(artist_select.options[artist_select.selectedIndex].value);
  var loc_select = document.getElementById( "location");
  var edit_location = parseInt(loc_select.options[loc_select.selectedIndex].value);
  var edit_date = parseInt(document.getElementById("creation-date-sidenav").value);
  var edit_medium = document.getElementById("medium-sidenav").value;
  var edit_description = document.getElementById("art-description-sidenav").value;
  var edit_height = parseFloat(document.getElementById("dimensions-height-cm-sidenav").value);
  var edit_width = parseFloat(document.getElementById("dimensions-width-cm-sidenav").value);
  var edit_type = document.getElementById("type-sidenav").value;
  var edit_bid = parseInt(document.getElementById("bid").value);

  dataObject = {
    "artID": artID,
    "artistID": edit_artist,
    "artTitle": edit_title,
    "artDescription": edit_description,
    "artType": edit_type,
    "artHeight": edit_height,
    "artWidth": edit_width,
    "artDepth": 12.00,
    "artMedium": edit_medium,
    "artYear": edit_date,
    "locationID": edit_location,
    "artMainImage": null,
    "artForSale": edit_bid,
  }

  $.ajax({
      url: "/api/art/" + artID,
      type: 'PUT',    
      data: JSON.stringify(dataObject),
      contentType: 'application/json',
      success: function(result) {
          window.location.href = '/art/' + artID;
      },
      error: function() {
          console.log("error")
      }
  });
}
