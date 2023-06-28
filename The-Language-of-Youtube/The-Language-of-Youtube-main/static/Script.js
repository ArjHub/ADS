function findGenre() {
  var title = document.getElementById('video-title').value;
  var description = document.getElementById('video-description').value;

  // Create a JSON object with the input data
  var data = {
    'title': title,
    'description': description
  };

  // Send the AJAX request to the Flask server
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/predict', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function () {
    if (xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      var genre = response.genre;
      document.getElementById('genre').textContent = 'Genre: ' + genre;
    } else {
      var error = JSON.parse(xhr.responseText);
      document.getElementById('genre').textContent = 'Error: ' + error.message;
    }
  };
  xhr.send(JSON.stringify(data));
}