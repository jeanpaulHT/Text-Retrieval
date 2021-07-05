$(function () {   
    $('#search').click(function() {
        var query = $("#query").val();
        var makequery = JSON.stringify({
              "query":query
                });
        $.ajax({
          url: '/search',
          type: 'POST',
          contentType: 'application/json',
          data : makequery,
          dataType:'json',
          success: function(data){
            results = document.getElementById("tweets");
            results.innerHTML = "";
            console.log(data)
            var datos = JSON.parse(data)
            console.log(datos)
              for (tweet of datos) {
           twttr.widgets.createTweet(tweet, results);
              }
          },   
          error: function(data){
              console.log(data);
          }
        });
      });
})