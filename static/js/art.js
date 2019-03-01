function writeArtToDOM(response) {
	var response_obj = response;
	console.log(response_obj);
	document.getElementById("art-title-header").innerHTML = response_obj.art.artTitle;
	document.getElementById("art-title-sidenav").innerHTML = response_obj.art.artTitle;
	document.getElementById("art-artist-header").innerHTML = response_obj.artist.artistName;
	document.getElementById("artist-info-sidenav").innerHTML = response_obj.artist.artistName;
	document.getElementById("artist-info-sidenav").href = "/artist/" + response_obj.artist.artistID;
	document.getElementById("location-sidenav").innerHTML = response_obj.location.locationName;
	document.getElementById("location-sidenav").href = "/location/" + response_obj.location.locationID;
	document.getElementById("location-city-sidenav").innerHTML = ", " + response_obj.location.locationCity;
	document.getElementById("creation-date-sidenav").innerHTML = response_obj.art.artYear;
	document.getElementById("medium-sidenav").innerHTML = response_obj.art.artMedium;
	document.getElementById("art-description-sidenav").innerHTML = response_obj.art.artDescription;
	document.getElementById("art-main-image").src = "../static/img/" + response_obj.images.artMainImage;
	if(response_obj.bids.artForSale != 0){
		if(response_obj.bids.bidHighestAmount != null){
			document.getElementById("biddable").innerHTML = "This artwork has already been sold!<br> The winning bid was $" + response_obj.bids.bidHighestAmount + ".<br><br>"
		}
	}
	/*if(response_obj.bids.artForSale != 0){
		if(response_obj.bids.bidDirectSale != 0){
			document.getElementById("biddable").innerHTML = "This artwork is currently for sale!<br> You can directly purchase it for $" + response_obj.bids.bidStartingAmount + ".<br><br>"
			var button = document.createElement('input');
        	button.setAttribute('type', 'submit');
        	button.setAttribute('ID', 'purchase');
        	button.setAttribute('value', 'Purchase Now');
        	button.addEventListener('click', function(){
        		dataObject = {
    				"Name": "Jack Callahan",
    				"bid": response_obj.bids.bidStartingAmount,
    				"QQQ": "QQQ",
  				}
        		$.ajax({
    				url: "/api/bid",
    				type: 'POST',    
    				data: JSON.stringify(dataObject),
    				contentType: 'application/json',
    				success: function(result) {
      					alert("Thank you for your interest in this artwork. Someone from our staff will contact you within 24 hours with more information.");
    				},
    				error: function() {
      					alert("Error saving data. Please try again.");
    				}
  				});
        	});
        	document.getElementById("biddable").appendChild(button)
		}
		else if(response_obj.bids.bidHighestAmount != null){
			//TODO: add a default value and submit function. This function checks min increment and sanitizes input before posting
			document.getElementById("biddable").innerHTML = "This artwork is currently for sale!<br> The current highest bid is $" + response_obj.bids.bidHighestAmount + ".<br><br>"
			var f = document.createElement("form");
			//f.setAttribute('method',"post");
			//f.setAttribute('action',"submit.php");

			var i = document.createElement("input"); //input element, text
			i.setAttribute('type',"text");
			i.setAttribute('name',"username");

			var s = document.createElement("input"); //input element, Submit button
			s.setAttribute('type',"submit");
			s.setAttribute('value',"Bid!");

			f.appendChild(i);
			f.appendChild(s);
			document.getElementById("biddable").appendChild(f)
		}
		else{
			//TODO: same as above!
			document.getElementById("biddable").innerHTML = "This artwork is currently for sale!<br> No one has bid yet, but the minimum bid is $" + response_obj.bids.bidStartingAmount + ".<br><br>"
			var f = document.createElement("form");
			//f.setAttribute('method',"post");
			//f.setAttribute('action',"submit.php");

			var i = document.createElement("input"); //input element, text
			i.setAttribute('type',"text");
			i.setAttribute('name',"username");

			var s = document.createElement("input"); //input element, Submit button
			s.setAttribute('type',"submit");
			s.setAttribute('value',"Bid!");

			f.appendChild(i);
			f.appendChild(s);
			document.getElementById("biddable").appendChild(f)
		}
	}*/
	var tags = response_obj.art.artTags;
    var tags_str = "";
    for (var i = 0; i < tags.length; i++) {
        tags_str += "<a href=#>" + tags[i].tagName + "</a>; ";
    }
    document.getElementById("art-tags").innerHTML = tags_str;
}

function renderArt(artID) {
  $.ajax('/api/art/' + artID, {
    type: "GET",
    success: function(data, textStatus, jqXHR) {
      var response = data;
      writeArtToDOM(response);
    },
    error: function(data, textStatus, jqXHR) {
      console.log("error");
    }

  });
}