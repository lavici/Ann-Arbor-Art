function writeAllArtistToDOM(response) {
  var res = response['artists'];
  var artist_amount = res.length;
  var append_str = "";
  for (var i = 0; i < artist_amount; i++) {
    if (res[i]['artistImage'] == null) {
      res[i]['artistImage'] = "no_artist_img.png";
    }
    append_str += "<div class='row'><div class='col-md-3'> <a href='/artist/" + res[i]['artistID'] + "'> <img class='img-fluid rounded md-3 mb-md-0' src='../static/img/" + res[i]['artistImage'] + "' alt=''> </a> </div> <div class='col-md-9'> <h3>" + res[i]['artistPreferredName'] + "</h3><p id='art_id_" + res[i]['artistID'] + "'></p><a class='btn btn-info' href='/artist/" + res[i]['artistID'] + "'>more on the artist</a></div></div><hr>";
  }
  document.getElementById("js_entry").innerHTML = append_str;
  for (var i = 0; i < artist_amount; i++) {
    var id_bio = "art_id_" + res[i]['artistID'];
    document.getElementById(id_bio).innerHTML = res[i]["artistBio"];
  }
}


function renderAllArtists() {
  $.ajax('/api/artists', {
    type: "GET",
    success: function(data, textStatus, jqXHR) {
      var response = data;
      writeAllArtistToDOM(response);
    },
    error: function(data, textStatus, jqXHR) {
      console.log("404 Error Redirect");
    }
  });
}
