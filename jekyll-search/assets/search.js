(function() {
    var request = new XMLHttpRequest();
    var searchBox = document.getElementById("search-box");
    var resultBox = document.getElementById("search-results");
    var posts;
    var results;
    var html = "";

    request.onreadystatechange = function(e) {

        // the request is done and successful.
        if (request.readyState === 4 && request.status === 200) {

            // parse the json response in to an array of objects.
            posts = JSON.parse(request.responseText);

            // filter the posts to those who's title contains text from the search box.
            results = posts.filter(function(post) {
                if (post.title.toLowerCase().indexOf(searchBox.value.trim().toLowerCase()) > -1) {
                    return true;
                }
            });

            // if there are results, show a list item and link for each result.
            if (results.length > 0 && searchBox.value.trim() != "") {
                html += "<ul>";
                for (var i = 0; i < results.length; i++) {
                    html += "<li><a href=\"" + results[i].url + "\">" + results[i].title + "</a></li>";
                }
                html += "</ul>";

                resultBox.innerHTML = html;
            }
        }
    };

    // detect input on the search box.
    searchBox.onkeyup = function(e) {
        resultBox.innerHTML = "";
        html = "";
        results = [];
        request.open("GET", "/search.json");
        request.send();
    };
})();
