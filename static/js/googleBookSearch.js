$(document).ready(function() {
    $("#search").click(
      function() {
        $.get('/get_meta_data', {
            title: $("#title").val(), 
            author: $("#author").val(),
            isbn: $("#isbn").val(),
        }, function(resultString, textStatus, jqXHR) {
            $("#greeting").addClass("hidden");
            var results = jQuery.parseJSON(resultString);
            resultsContainer = $("#searchResults");
            results.forEach(function(book) {
                entry = $("<div><span style=\"font-style: italic\">" + book.title + "</span>, " + book.authors + " </div>");
                button = $("<button />", {
                    text: "This One!",
                    click: function() {
                            console.log(results);
                            $("#title").val(book.title);
                            $("#author").val(book.authors);
                            $("#isbn").val(book.isbn);
                            $("#publisher").val(book.publisher);
                            $("#publishedDate").val(book.publishedDate);
                            $("#searchForm").removeClass("hidden");
                            $("#searchResults").empty();
                    }});
                resultsContainer.append(entry);
                entry.append(button);
                })
            });
    });
    });

