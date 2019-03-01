/*
The function renderAll is called on the load of list.html. It takes in parameters
cols, which is the number of columns created that are in list.html, col_size, which
is the number of images to put into each column, and db_size, which is the number of images
in the database. It creates divs of the format below and appends them to the columns.
Images are randomly chosen from the database.

<div id="thumb">
		  		<a href="/art" style="text-decoration: none; color:white;">
			    	<img id="thumb-border" src="../static/img/5.jpg" style="width:100%">
			    	<div style="text-indent: 5%;">The French Set, 1858</div>
			    	<div style="text-indent: 5%; font-style: normal;">James Abbott McNeill Whistler</div>
			    </a>
			</div>

*/

function shuffle(array) {
  var currentIndex = array.length, temporaryValue, randomIndex;

  // While there remain elements to shuffle...
  while (0 !== currentIndex) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex -= 1;

    // And swap it with the current element.
    temporaryValue = array[currentIndex];
    array[currentIndex] = array[randomIndex];
    array[randomIndex] = temporaryValue;
  }

  return array;
}


function writeArtToDOM(col, response) {
	var response_obj = response;
	//console.log(response_obj);
	// Get column object
	var col = document.getElementById("col_" + col);
	// Create the container that we will append data to
	var artObject = document.createElement('div');
	artObject.id = 'thumb';
	artObject.class = 'thumbnails'
	// Create the link w/ the ID of the piece of art
	var link = document.createElement('a')
	link.href = "/art/" + response_obj.art.artID
	link.style="text-decoration: none; color:white;"
	// Add the main image from the response 
	var img = document.createElement('img');
	if (typeof response_obj.art.artMainImage != 'undefined'){
		img.src = "../static/img/" + response_obj.art.artMainImage;
	}else{
		img.src = "../static/img/" + response_obj.images.artMainImage;
	}
	img.id = "thumb-border"
	img.style="width:100%"
	link.appendChild(img);

	// Add the piece's title and year
	var title = document.createElement('div');
	if(response_obj.art.artYear === null){
		title.appendChild(document.createTextNode(response_obj.art.artTitle));
	}else{
		title.appendChild(document.createTextNode(response_obj.art.artTitle + ", " + response_obj.art.artYear))
	}
	title.style="text-indent: 5%;";
	link.appendChild(title)
	// Add the artist name
	var artist = document.createElement('div');
	artist.appendChild(document.createTextNode(response_obj.artist.artistName))
	artist.style = "text-indent: 5%; font-style: normal;"
	link.appendChild(artist)
	artObject.appendChild(link);
	// Add everything to the original column
	col.appendChild(artObject);
}

function resetCols(num_cols) {
	for(i = 1; i <= num_cols; i++){
		var myNode = document.getElementById("col_" + i);
		console.log(myNode)
		while (myNode.firstChild) {
    		myNode.removeChild(myNode.firstChild);
		}
	}
}

function renderNearby(){
	resetCols(3)
	let arr = [1, 2, 7]
	for(i = 0; i < 3; i++){
		//var num = Math.floor(Math.random() * db_size + 1);
		var num = (i % 3) + 1
		renderArt(num, arr[i]);
	}
}

function renderSale(){
	resetCols(3)
	let arr = [3, 4, 5, 6, 7, 8, 9]
	for(i = 0; i < 7; i++){
		var num = (i % 3) + 1
		renderArt(num, arr[i])
	}
}

function renderRecent(){
	resetCols(3)
	let arr = [3, 4, 5]
	for(i = 0; i < 3; i++){
		var num = (i % 3) + 1
		renderArt(num, arr[i])
	}
}

function renderArt(col, artID) {
  $.ajax('/api/art/' + artID, {
    type: "GET",
    success: function(data, textStatus, jqXHR) {
      var response = data;
      writeArtToDOM(col, response);
    },
    error: function(data, textStatus, jqXHR) {
      console.log("error");
    }

  });
}

function renderAll(cols, col_size, db_size) {
	for(i = 1; i <= col_size * cols; i++){
		//var num = Math.floor(Math.random() * db_size + 1);
		var num = (i % 3) + 1
		renderArt(num, i);
	}

}

function reRender() {
	resetCols(3)
	renderAllArt()
}

function renderAllArt() {
  $.ajax('/api/artworks', {
    type: "GET",
    success: function(data, textStatus, jqXHR) {
      var response = data;
      for(i = 0; i < response.artwork.length; i++){
      	writeArtToDOM(i%3 + 1, response.artwork[i])
      }
    },
    error: function(data, textStatus, jqXHR) {
      console.log("error");
    }

  });
}