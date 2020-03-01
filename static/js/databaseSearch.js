$(document).ready(function() {
    $("#search").click(
      function() {
        $.get('/browse', {
            title: $("#title").val(), 
            author: $("#author").val(),
            isbn: $("#isbn").val(),
        }, function(resultString, textStatus, jqXHR) {
            $("#greeting").addClass("hidden");
            var results = jQuery.parseJSON(resultString);
            resultsContainer = $("#searchResults");
            results.forEach(function(book) {
                entry = $("<div><span style=\"font-style: italic\">" + book.title + "</span>, " + book.author + " </div>");
                resultsContainer.append(entry);
                })
            });
    });
    });
