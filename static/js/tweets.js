$(function () {   
    $('#search').click(function() {
        var query = $("#query").val();
        var makequery = JSON.stringify({
              "query":query
                });
        $.ajax({
              url: '/search',
              type: 'post',
              contentType: 'application/json',
              data : makequery,
              dataType:'json',
              success: function(data){
                results = document.getElementById('tweets');
                results.innerHTML = "";
                  for (tweet of data) {
                    twttr.widgets.createTweet(tweet, results).then( function( el ) {
                      console.log('Tweet added.');
                    });
                  }
              },   
              error: function(data){
                  console.log(data);
              }
            });
      });
})