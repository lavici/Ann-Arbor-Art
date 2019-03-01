var cur = -1
function onSignIn(googleUser) {
    console.log("signed_in")
    var profile = googleUser.getBasicProfile();
    var newDiv = document.createElement("div");
    // var newContent = document.createTextNode("Hi " + profile.getName() + "!");
    // newDiv.appendChild(newContent);  
    newDiv.setAttribute("id", "name")
    newDiv.setAttribute("class", "hidden")
    // add the newly created element and its content into the DOM 
    var currentDiv = document.getElementById("name"); 
    document.body.insertBefore(newDiv, currentDiv);
    unhide("name")
    // hide("signin")
    // unhide("user_dropdown")
    document.getElementById("signin").style.visibility = "hidden"
    document.getElementById("user_dropdown").style.visibility = "visible"
    
    // call login api to populate database with user info
    dataObject = {
        "username": profile.getEmail().substring(0, profile.getEmail().lastIndexOf("@")),
        "firstName": profile.getName().substring(0, profile.getName().lastIndexOf(' ')),
        "lastName": profile.getName().substring(profile.getName().lastIndexOf(' ')+1),
        "phone": ""
    }
    $.ajax({
        url: "/api/login",
        type: 'POST',    
        data: JSON.stringify(dataObject),
        contentType: 'application/json',
        success: function(result) {
            console.log(result)
        }
    });
}

function initMap() {
  //Center of map
  var uluru = {lat: 42.279991, lng: -83.745624};
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,
    center: uluru
  });
  var infowindow = new google.maps.InfoWindow();
  var service = new google.maps.places.PlacesService(map);
  //Get all locations
  $.ajax('/api/locations', {
    type: "GET",
    success: function(data, textStatus, jqXHR) {
      let response = data;
      for(i = 0; i < response.locations.length; i++){
        let locationID = response.locations[i].locationID
        //Add a pin for each location
        $.ajax('/api/location/' + locationID, {
          type: "GET",
          success: function(data, textStatus, jqXHR) {
            let artworkID1 = 0
            console.log(data)
            let artImage1 = 0
            if (data.artwork.artwork.length != 0){
              artworkID1 = data.artwork.artwork["0"].artID
              artImage1 = data.artwork.artwork["0"].artMainImage
              let artworkID2 = -1
              let artImage2 = 0
              if(data.artwork.artwork.length >= 2){
                artworkID2 = data.artwork.artwork["1"].artID
                artImage2 = data.artwork.artwork["1"].artMainImage
              }
              service.getDetails({
                placeId: response.locations[++cur].locationGooglePlaceID
              }, 
              function(place, status) {
                if (status === google.maps.places.PlacesServiceStatus.OK) {
                  let marker = new google.maps.Marker({
                    map: map,
                    position: place.geometry.location,
                  });
                  google.maps.event.addListener(marker, 'click', function() {
                    let image = '<a href="/art/' + artworkID1 +'"><img src="static/img/' + artImage1 + '" style="width:100px;height:100px;"></a>  '
                    if(data.artwork.artwork.length >= 2){
                      image += '<a href = "/art/' + artworkID2 + '"><img src="static/img/' + artImage2 + '" style="width:100px;height:100px;"></a>'
                    }
                    let content = '<div><strong><a href=/location/' + locationID + '>' + place.name + '</strong></a><br>' + image + '<br><a href=https://www.google.com/maps/search/?api=1&query=' + encodeURI(place.name) + '>' + place.formatted_address + '</a></div>'
                    
                    infowindow.setContent(content);
                    infowindow.open(map, this);
                  });
                }
              });
            }
          },error: function(data, textStatus, jqXHR) {
            console.log("error");
          }
        })
      }
    },
    error: function(data, textStatus, jqXHR) {
      console.log("error");
    }
  });
}

  function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      unhide("ArtHub")
  	  unhide("map")
  	  unhide("signout")
  	  unhide("name")
      unhide("signin")
      unhide("welcome")
    });
  }

function unhide(divID) {
var item = document.getElementById(divID);
if (item) {
    if(item.className=='hidden'){
        item.className = 'unhidden' ;
    }else{
        item.className = 'hidden' ;
    }if(divID=="map"){
    	initMap()
    }
}}
    
function hide(divID) {
var item = document.getElementById(divID);
if (item) {
    if(item.className=='unhidden'){
        item.className = 'hidden' ;
    }else{
        item.className = 'hidden' ;
    }
}}

var favorited = false;

 function changeFavoriteToGold(clicked) {
      var x = $("#star");
      x.text("★");
      x[0].style.color = 'gold';
      if (clicked) favorited = true;
  }

function changeFavoriteToNormal() {
    if (!favorited){
      var x = $("#star");
      x.text("☆");
      x[0].style.color = 'black';
    }
}

