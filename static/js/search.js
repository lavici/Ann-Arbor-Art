// JS file for Search

function renderSearch(){
	var query = getSearchParams("q");

	$.ajax('/api/search?q=' + encodeURIComponent(query), {
	    type: "GET",
	    success: function(data, textStatus, jqXHR) {
	      var response = data;
	      writeSearchToDOM(response);
	    },
	    error: function(data, textStatus, jqXHR) {
	      writeNoResultsToDOM();
	      console.log("error");
	    }
	});
}

function getSearchParams(k){
 var p={};
 location.search.replace(/[?&]+([^=&]+)=([^&]*)/gi,function(s,k,v){p[k]=v})
 return k?p[k]:p;
}

$('.search').keypress(function (e) {
  if (e.which == 13) {
    $('form#search-form').submit();
    return false;
  }
});

function writeNoResultsToDOM(){
	var artObject = document.createElement('div');
	artObject.id = 'thumb';
	if (getSearchParams("q")){
		artObject.appendChild(document.createTextNode("No Search Results."));
	}
	else{
		artObject.appendChild(document.createTextNode("Empty search, please try another search"));
	}
	var row = document.getElementById("search-row");
	row.appendChild(artObject);
}

function writeSearchToDOM(response) {
	var response_obj = response;
	console.log(response_obj);

	// Get column object
	var res = response['searchResults'];
	var search_size = res.length;
	var append_str = "";
	if (search_size == 0){
		var artObject = document.createElement('div');
		artObject.id = 'thumb';
		artObject.appendChild(document.createTextNode("No Search Results."));
		var row = document.getElementById("search-row");
		row.appendChild(artObject);
	}

	for (var i = 0; i < search_size; i++) {
		// Get column object
		var col = document.getElementById("col_" + (i + 1) % 3);

		// Create the container that we will append data to
		var artObject = document.createElement('div');
		artObject.id = 'thumb';

		// Create the link w/ the ID of the piece of art
		var link = document.createElement('a')
		link.href = "/art/" + response_obj.searchResults[i].art.artID
		link.style="text-decoration: none; color:white;"

		// Add the main image from the response 
		var img = document.createElement('img');
		img.src = "../static/img/" + response_obj.searchResults[i].art.artMainImage;
		img.id = "thumb-border"
		img.style="width:100%"
		link.appendChild(img);

		// Add the piece's title and year
		var title = document.createElement('div');
		if(response_obj.searchResults[i].art.artYear === null){
			title.appendChild(document.createTextNode(response_obj.searchResults[i].art.artTitle));
		}else{
			title.appendChild(document.createTextNode(response_obj.searchResults[i].art.artTitle + ", " + response_obj.searchResults[i].art.artYear));
		}
		title.style="text-indent: 5%;";
		link.appendChild(title)

		// Add the artist name
		var artist = document.createElement('div');
		artist.appendChild(document.createTextNode(response_obj.searchResults[i].artist.artistName))
		artist.style = "text-indent: 5%; font-style: normal;"
		link.appendChild(artist)
		artObject.appendChild(link);

		// Add everything to the original column
		col.appendChild(artObject);
	}
}
		